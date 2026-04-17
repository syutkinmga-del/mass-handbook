import { useMemo, useState, useEffect } from 'react';

export interface PaperMetadata {
  id: string;
  title: string;
  tags: string[];
}

/**
 * Хук для загрузки метаданных статей из JSON файла
 */
export function usePaperTags(): PaperMetadata[] {
  const [papers, setPapers] = useState<PaperMetadata[]>([]);

  useEffect(() => {
    // Загружаем данные о статьях из JSON файла
    fetch('/papers-data.json')
      .then((response) => response.json())
      .then((data) => setPapers(data))
      .catch((error) => console.error('Failed to load papers data:', error));
  }, []);

  return papers;
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
