import React, { useMemo } from 'react';
import type { Props } from '@theme/DocSidebar/Mobile';
import DocSidebarMobile from '@theme-original/DocSidebar/Mobile';
import { useTagFilter } from '@site/src/contexts/TagFilterContext';
import { usePaperTags, getHiddenDocIds } from '@site/src/hooks/usePaperTags';

/**
 * Компонент для фильтрации мобильного сайдбара на основе выбранных тегов
 * Использует JSON файл с метаданными статей для фильтрации
 */
export default function DocSidebarMobileWrapper(props: Props): JSX.Element {
  const { selectedTags, hasAnyTagSelected } = useTagFilter();
  const papers = usePaperTags();

  // Если теги не выбраны или данные не загружены, показываем сайдбар как есть
  if (!hasAnyTagSelected || papers.length === 0) {
    return <DocSidebarMobile {...props} />;
  }

  // Получаем список документов, которые нужно скрыть
  const hiddenDocIds = useMemo(() => {
    return getHiddenDocIds(papers, selectedTags);
  }, [papers, selectedTags]);

  // Фильтруем элементы сайдбара на основе скрытых документов
  const filteredSidebar = useMemo(() => {
    return filterSidebarItems(props.sidebar, hiddenDocIds);
  }, [props.sidebar, hiddenDocIds]);

  return <DocSidebarMobile {...props} sidebar={filteredSidebar} />;
}

/**
 * Рекурсивно фильтрует элементы сайдбара
 */
function filterSidebarItems(items: any[], hiddenDocIds: Set<string>): any[] {
  return items
    .map((item) => {
      // Если это категория, рекурсивно фильтруем её элементы
      if (item.type === 'category' && item.items) {
        const filteredItems = filterSidebarItems(item.items, hiddenDocIds);
        
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

      // Если это документ (статья), проверяем, нужно ли его скрывать
      if (item.type === 'doc') {
        const docId = item.id || extractDocIdFromItem(item);
        
        // Если документ скрыт, пропускаем его
        if (docId && hiddenDocIds.has(docId)) {
          return null;
        }
        
        return item;
      }

      // Для других типов элементов показываем как есть
      return item;
    })
    .filter((item) => item !== null);
}

/**
 * Извлекает ID документа из объекта элемента сайдбара
 */
function extractDocIdFromItem(item: any): string | null {
  if (item.id) {
    return item.id;
  }

  if (item.docId) {
    return item.docId;
  }

  if (item.href) {
    const match = item.href.match(/\/docs\/papers\/([^/]+)$/);
    if (match) {
      return match[1];
    }
  }

  return null;
}
