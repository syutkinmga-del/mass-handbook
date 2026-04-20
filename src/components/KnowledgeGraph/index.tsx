import React, { useEffect, useRef, useMemo } from 'react';
import styles from './styles.module.css';

interface Node {
  id: string;
  label: string;
  type: 'paper' | 'tag';
  color: string;
  size: number;
}

interface Link {
  source: string;
  target: string;
}

interface KnowledgeGraphProps {
  maxPapers?: number;
  maxTags?: number;
}

export default function KnowledgeGraph({ maxPapers = 10, maxTags = 15 }: KnowledgeGraphProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const graphData = useMemo(() => {
    // Simplified graph data based on papers and tags
    const tagFrequency: Record<string, number> = {
      'Collision Avoidance': 10,
      'MASS': 8,
      'Decision Making': 7,
      'Genetic Algorithm': 7,
      'User Interface': 6,
      'Dynamic Window Approach': 5,
      'Path Planning': 4,
      'Knowledge Representation': 4,
      'Compliance': 3,
      'Trajectory Planning': 3,
      'Obstacle Avoidance': 3,
      'Safety': 2,
      'Deep Reinforcement Learning': 2,
      'Reinforcement Learning': 2,
      'Situational Awareness': 2,
    };

    const paperTags: Record<string, string[]> = {
      'paper_0001': ['COLREGs', 'Collision Avoidance', 'Path Planning'],
      'paper_0002': ['Collision Avoidance', 'Dynamic Window Approach'],
      'paper_0004': ['Collision Avoidance', 'Deep Reinforcement Learning', 'Path Planning'],
      'paper_0005': ['Collision Avoidance', 'Safety', 'MASS'],
      'paper_0008': ['Knowledge Representation', 'Situational Awareness'],
      'paper_0010': ['Dynamic Window Approach', 'Path Planning', 'MASS'],
      'paper_0013': ['Deep Reinforcement Learning', 'Path Planning', 'Trajectory Planning'],
    };

    const nodes: Node[] = [];
    const links: Link[] = [];
    const nodeIds = new Set<string>();

    // Add tag nodes
    Object.entries(tagFrequency)
      .slice(0, maxTags)
      .forEach(([tag, count]) => {
        const nodeId = `tag_${tag}`;
        nodes.push({
          id: nodeId,
          label: tag,
          type: 'tag',
          color: '#4a9eff',
          size: 3 + (count / 10) * 7,
        });
        nodeIds.add(nodeId);
      });

    // Add paper nodes and links
    Object.entries(paperTags)
      .slice(0, maxPapers)
      .forEach(([paper, tags]) => {
        const nodeId = `paper_${paper}`;
        nodes.push({
          id: nodeId,
          label: paper.replace('paper_', 'P'),
          type: 'paper',
          color: '#ff6b6b',
          size: 5,
        });
        nodeIds.add(nodeId);

        // Create links to tags
        tags.forEach((tag) => {
          const tagNodeId = `tag_${tag}`;
          if (nodeIds.has(tagNodeId)) {
            links.push({
              source: nodeId,
              target: tagNodeId,
            });
          }
        });
      });

    return { nodes, links };
  }, [maxPapers, maxTags]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    const rect = containerRef.current?.getBoundingClientRect();
    if (!rect) return;

    canvas.width = rect.width;
    canvas.height = rect.height;

    // Simple force-directed graph simulation
    const nodes = graphData.nodes.map((node) => ({
      ...node,
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: 0,
      vy: 0,
    }));

    const animate = () => {
      // Clear canvas
      ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--color-bg');
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw links
      ctx.strokeStyle = 'rgba(100, 100, 100, 0.2)';
      ctx.lineWidth = 1;
      graphData.links.forEach((link) => {
        const source = nodes.find((n) => n.id === link.source);
        const target = nodes.find((n) => n.id === link.target);
        if (source && target) {
          ctx.beginPath();
          ctx.moveTo(source.x, source.y);
          ctx.lineTo(target.x, target.y);
          ctx.stroke();
        }
      });

      // Draw nodes
      nodes.forEach((node) => {
        ctx.fillStyle = node.color;
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.size, 0, Math.PI * 2);
        ctx.fill();

        // Draw label
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 10px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(node.label, node.x, node.y);
      });

      requestAnimationFrame(animate);
    };

    animate();
  }, [graphData]);

  return (
    <div className={styles.graphContainer}>
      <h2 className={styles.title}>Граф знаний</h2>
      <p className={styles.description}>
        Визуализация связей между статьями (красные узлы) и тегами (синие узлы). Размер узла указывает на популярность.
      </p>
      <div className={styles.canvasWrapper} ref={containerRef}>
        <canvas ref={canvasRef} className={styles.canvas} />
        <div className={styles.legend}>
          <div className={styles.legendItem}>
            <div className={`${styles.legendDot} ${styles.paper}`}></div>
            <span>Статья</span>
          </div>
          <div className={styles.legendItem}>
            <div className={`${styles.legendDot} ${styles.tag}`}></div>
            <span>Тег</span>
          </div>
        </div>
      </div>
      <p className={styles.note}>
        <em>Граф визуализирует топ-10 статей и топ-15 тегов. Связи показывают, какие теги присвоены каждой статье.</em>
      </p>
    </div>
  );
}
