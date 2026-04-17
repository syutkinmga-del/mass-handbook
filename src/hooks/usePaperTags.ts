import { useMemo } from 'react';

interface PaperMetadata {
  title: string;
  tags: string[];
  path: string;
}

/**
 * Хук для работы с метаданными статей
 * В реальном приложении эти данные могут загружаться из API или статического JSON
 */
export function usePaperTags(): PaperMetadata[] {
  // Это временное решение - в идеале данные должны быть загружены из Docusaurus API
  // или из статического JSON файла, который генерируется при сборке
  const papers = useMemo(() => {
    // Здесь должны быть реальные данные из статей
    // Для теперь возвращаем пустой массив, так как Docusaurus не предоставляет прямого доступа к метаданным
    return [];
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
