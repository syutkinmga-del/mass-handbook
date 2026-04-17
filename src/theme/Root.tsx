import React, { ReactNode } from 'react';
import { TagFilterProvider } from '@site/src/contexts/TagFilterContext';

interface RootProps {
  children: ReactNode;
}

/**
 * Корневой компонент, который обеспечивает доступ к TagFilterContext
 * для всех компонентов приложения
 */
export default function Root({ children }: RootProps): JSX.Element {
  return (
    <TagFilterProvider>
      {children}
    </TagFilterProvider>
  );
}
