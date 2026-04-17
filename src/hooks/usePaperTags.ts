import { papersData, type PaperMetadata } from '@site/src/data/papersData';

/**
 * Хук для получения метаданных статей
 * Использует встроенные данные вместо загрузки из JSON
 */
export function usePaperTags(): PaperMetadata[] {
  return papersData;
}

/**
 * Фильтрует статьи по выбранным тегам
 */
export function filterPapersByTags(
  papers: PaperMetadata[],
  selectedTags: Set<string>
): PaperMetadata[] {
  if (selectedTags.size === 0) {
    return papers;
  }

  return papers.filter((paper) =>
    paper.tags.some((tag) => selectedTags.has(tag))
  );
}

/**
 * Возвращает список документов, которые нужно скрыть при фильтрации
 */
export function getHiddenDocIds(
  papers: PaperMetadata[],
  selectedTags: Set<string>
): Set<string> {
  if (selectedTags.size === 0) {
    return new Set();
  }

  const visiblePapers = filterPapersByTags(papers, selectedTags);
  const visibleIds = new Set(visiblePapers.map((p) => p.id));

  return new Set(
    papers
      .map((p) => p.id)
      .filter((id) => !visibleIds.has(id))
  );
}

export type { PaperMetadata };
