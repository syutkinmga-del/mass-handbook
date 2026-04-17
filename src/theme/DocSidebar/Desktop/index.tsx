import React, { useMemo } from 'react';
import type { Props } from '@theme/DocSidebar/Desktop';
import DocSidebarDesktop from '@theme-original/DocSidebar/Desktop';
import { useTagFilter } from '@site/src/contexts/TagFilterContext';

/**
 * Компонент для фильтрации сайдбара на основе выбранных тегов
 * Скрывает статьи, которые не содержат выбранные теги
 */
export default function DocSidebarDesktopWrapper(props: Props): JSX.Element {
  const { selectedTags, hasAnyTagSelected } = useTagFilter();

  // Если теги не выбраны, показываем сайдбар как есть
  if (!hasAnyTagSelected) {
    return <DocSidebarDesktop {...props} />;
  }

  // Фильтруем элементы сайдбара на основе выбранных тегов
  const filteredSidebar = useMemo(() => {
    return filterSidebarItems(props.sidebar, selectedTags);
  }, [props.sidebar, selectedTags]);

  return <DocSidebarDesktop {...props} sidebar={filteredSidebar} />;
}

/**
 * Рекурсивно фильтрует элементы сайдбара
 */
function filterSidebarItems(items: any[], selectedTags: Set<string>): any[] {
  return items
    .map((item) => {
      // Если это категория, рекурсивно фильтруем её элементы
      if (item.type === 'category' && item.items) {
        const filteredItems = filterSidebarItems(item.items, selectedTags);
        
        // Если в категории остались элементы, возвращаем её
        if (filteredItems.length > 0) {
          return {
            ...item,
            items: filteredItems,
          };
        }
        
        // Если в категории нет элементов, пропускаем её
        return null;
      }

      // Если это документ (статья), проверяем её теги
      if (item.type === 'doc') {
        const docTags = extractTagsFromDoc(item);
        
        // Если статья содержит хотя бы один из выбранных тегов, показываем её
        if (docTags.length > 0 && docTags.some((tag) => selectedTags.has(tag))) {
          return item;
        }

        // Если статья не содержит выбранные теги, пропускаем её
        return null;
      }

      // Для других типов элементов (ссылки, разделители и т.д.) показываем как есть
      return item;
    })
    .filter((item) => item !== null);
}

/**
 * Извлекает теги из документа
 * Это временное решение - в реальном приложении теги должны быть доступны через API
 */
function extractTagsFromDoc(doc: any): string[] {
  // Попытаемся получить теги из различных источников
  if (doc.tags && Array.isArray(doc.tags)) {
    return doc.tags;
  }

  if (doc.metadata?.tags && Array.isArray(doc.metadata.tags)) {
    return doc.metadata.tags;
  }

  if (doc.frontMatter?.tags && Array.isArray(doc.frontMatter.tags)) {
    return doc.frontMatter.tags;
  }

  return [];
}
