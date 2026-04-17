import React, { useMemo } from 'react';
import type { Props } from '@theme/DocSidebar/Desktop';
import DocSidebarDesktop from '@theme-original/DocSidebar/Desktop';
import { useTagFilter } from '@site/src/contexts/TagFilterContext';
import { usePaperTags, getHiddenDocIds } from '@site/src/hooks/usePaperTags';

/**
 * Компонент для фильтрации сайдбара на основе выбранных тегов
 * Использует JSON файл с метаданными статей для фильтрации
 */
export default function DocSidebarDesktopWrapper(props: Props): JSX.Element {
  const { selectedTags, hasAnyTagSelected } = useTagFilter();
  const papers = usePaperTags();

  // Если теги не выбраны или данные не загружены, показываем сайдбар как есть
  if (!hasAnyTagSelected || papers.length === 0) {
    return <DocSidebarDesktop {...props} />;
  }

  // Получаем список документов, которые нужно скрыть
  const hiddenDocIds = useMemo(() => {
    return getHiddenDocIds(papers, selectedTags);
  }, [papers, selectedTags]);

  // Фильтруем элементы сайдбара на основе скрытых документов
  const filteredSidebar = useMemo(() => {
    return filterSidebarItems(props.sidebar, hiddenDocIds);
  }, [props.sidebar, hiddenDocIds]);

  return <DocSidebarDesktop {...props} sidebar={filteredSidebar} />;
}

/**
 * Рекурсивно фильтрует элементы сайдбара, скрывая документы, которые не содержат выбранные теги
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

      // Для других типов элементов (ссылки, разделители и т.д.) показываем как есть
      return item;
    })
    .filter((item) => item !== null);
}

/**
 * Извлекает ID документа из объекта элемента сайдбара
 */
function extractDocIdFromItem(item: any): string | null {
  // Попытаемся получить ID из различных источников
  if (item.id) {
    return item.id;
  }

  if (item.docId) {
    return item.docId;
  }

  if (item.href) {
    // Извлекаем ID из URL, например: /docs/papers/paper_0001_cro
    const match = item.href.match(/\/docs\/papers\/([^/]+)$/);
    if (match) {
      return match[1];
    }
  }

  if (item.label) {
    // Последняя попытка - поиск по названию (не очень надежно)
    // Это может быть полезно для отладки
    return null;
  }

  return null;
}
