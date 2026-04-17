import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';

interface TagFilterContextType {
  selectedTags: Set<string>;
  toggleTag: (tag: string) => void;
  clearTags: () => void;
  setTags: (tags: string[]) => void;
  hasAnyTagSelected: boolean;
}

const TagFilterContext = createContext<TagFilterContextType | undefined>(undefined);

export function TagFilterProvider({ children }: { children: ReactNode }): JSX.Element {
  const [selectedTags, setSelectedTags] = useState<Set<string>>(new Set());

  const toggleTag = useCallback((tag: string) => {
    setSelectedTags((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(tag)) {
        newSet.delete(tag);
      } else {
        newSet.add(tag);
      }
      return newSet;
    });
  }, []);

  const clearTags = useCallback(() => {
    setSelectedTags(new Set());
  }, []);

  const setTags = useCallback((tags: string[]) => {
    setSelectedTags(new Set(tags));
  }, []);

  const hasAnyTagSelected = selectedTags.size > 0;

  return (
    <TagFilterContext.Provider
      value={{
        selectedTags,
        toggleTag,
        clearTags,
        setTags,
        hasAnyTagSelected,
      }}
    >
      {children}
    </TagFilterContext.Provider>
  );
}

export function useTagFilter(): TagFilterContextType {
  const context = useContext(TagFilterContext);
  if (context === undefined) {
    throw new Error('useTagFilter must be used within a TagFilterProvider');
  }
  return context;
}
