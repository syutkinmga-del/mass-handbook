import React, { useState, useEffect, useMemo } from 'react';
import type { Props } from '@theme/DocSidebar/Desktop';
import DocSidebarDesktop from '@theme-original/DocSidebar/Desktop';
import { papersData } from '@site/src/data/papersData';

const STORAGE_KEY = 'mass-handbook-selected-tags';

/**
 * Компонент для фильтрации сайдбара на основе выбранных тегов
 * Использует localStorage для синхронизации состояния фильтра
 */
export default function DocSidebarDesktopWrapper(props: Props): JSX.Element {
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [isClient, setIsClient] = useState(false);

  // Initialize from localStorage and listen for changes
  useEffect(() => {
    setIsClient(true);

    // Load initial tags from localStorage
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        const tags = JSON.parse(stored);
        setSelectedTags(tags);
      } catch (e) {
        console.error('Failed to parse stored tags:', e);
      }
    }

    // Listen for tag changes from filter component
    const handleTagsChanged = (event: CustomEvent) => {
      const tags = event.detail?.tags || [];
      setSelectedTags(tags);
    };

    window.addEventListener('tagsChanged', handleTagsChanged as EventListener);
    return () => {
      window.removeEventListener('tagsChanged', handleTagsChanged as EventListener);
    };
  }, []);

  // Create a map of paper IDs to their tags for quick lookup
  const paperTagsMap = useMemo(() => {
    const map = new Map<string, string[]>();
    papersData.forEach(paper => {
      map.set(paper.id, paper.tags);
    });
    return map;
  }, []);

  // Filter sidebar items based on selected tags
  const filteredSidebar = useMemo(() => {
    if (selectedTags.length === 0 || !isClient) {
      return props.sidebar;
    }

    const filterSidebarItems = (items: any[]): any[] => {
      return items
        .map(item => {
          // If it's a category/group, recursively filter its children
          if (item.items && Array.isArray(item.items)) {
            const filteredItems = filterSidebarItems(item.items);
            return filteredItems.length > 0 ? { ...item, items: filteredItems } : null;
          }

          // If it's a doc item, check if it matches the selected tags
          if (item.id) {
            const paperTags = paperTagsMap.get(item.id) || [];
            // Show item if it has ALL selected tags
            const hasAllTags = selectedTags.every(tag => paperTags.includes(tag));
            return hasAllTags ? item : null;
          }

          // Keep other items (links, etc.)
          return item;
        })
        .filter(Boolean);
    };

    return filterSidebarItems(props.sidebar);
  }, [selectedTags, props.sidebar, paperTagsMap, isClient]);

  return <DocSidebarDesktop {...props} sidebar={filteredSidebar} />;
}
