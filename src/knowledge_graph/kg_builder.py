"""
Knowledge Graph Builder / 知識圖譜構建器 / 知识图谱构建器
========================================================
Builds and manages knowledge graphs from NLU-extracted entities and relations.
從 NLU 提取的實體和關係構建並管理知識圖譜。
从 NLU 提取的实体和关系构建并管理知识图谱。

Integration Points / 接入點 / 接入点:
- NLU entities → graph nodes / NLU 實體 → 圖節點
- NLU relations → graph edges / NLU 關係 → 圖邊
- Graph → python-pptx visualization / 圖譜 → python-pptx 視覺化
- Graph → openpyxl adjacency export / 圖譜 → openpyxl 鄰接矩陣匯出
"""

from typing import Any

import networkx as nx


class KnowledgeGraphBuilder:
    """
    Knowledge graph construction and query engine.
    知識圖譜構建和查詢引擎。
    知识图谱构建和查询引擎。
    """

    def __init__(self):
        # Directed graph for entity relationships
        # 有向圖用於實體關係 / 有向图用于实体关系
        self.graph = nx.DiGraph()

    def add_entity(self, name: str, entity_type: str, **attributes: Any) -> None:
        """
        Add entity as graph node.
        新增實體作為圖節點。
        添加实体作为图节点。
        """
        self.graph.add_node(name, entity_type=entity_type, **attributes)

    def add_relation(
        self,
        subject: str,
        predicate: str,
        obj: str,
        confidence: float = 1.0,
    ) -> None:
        """
        Add relation as graph edge (subject -> object).
        新增關係作為圖邊（主語 → 賓語）。
        添加关系作为图边（主语 → 宾语）。
        """
        # Auto-create nodes if they don't exist
        if subject not in self.graph:
            self.graph.add_node(subject)
        if obj not in self.graph:
            self.graph.add_node(obj)

        self.graph.add_edge(subject, obj, predicate=predicate, confidence=confidence)

    def add_triples(self, triples: list[dict[str, str]]) -> None:
        """
        Batch add subject-predicate-object triples.
        批次新增主語-謂語-賓語三元組。
        批量添加主语-谓语-宾语三元组。
        """
        for triple in triples:
            self.add_relation(
                triple["subject"],
                triple["predicate"],
                triple["object"],
            )

    def get_neighbors(self, entity: str) -> list[dict[str, str]]:
        """
        Get all connected entities and their relations.
        取得所有連接的實體及其關係。
        获取所有连接的实体及其关系。
        """
        neighbors = []
        # Outgoing edges / 出邊
        for _, target, data in self.graph.out_edges(entity, data=True):
            neighbors.append({
                "direction": "outgoing",
                "entity": target,
                "predicate": data.get("predicate", ""),
            })
        # Incoming edges / 入邊
        for source, _, data in self.graph.in_edges(entity, data=True):
            neighbors.append({
                "direction": "incoming",
                "entity": source,
                "predicate": data.get("predicate", ""),
            })
        return neighbors

    def get_triples(self) -> list[dict[str, str]]:
        """
        Export all triples from the graph.
        從圖譜匯出所有三元組。
        从图谱导出所有三元组。
        """
        return [
            {
                "subject": u,
                "predicate": data.get("predicate", ""),
                "object": v,
            }
            for u, v, data in self.graph.edges(data=True)
        ]

    def to_adjacency_matrix(self) -> dict[str, Any]:
        """
        Export as adjacency matrix for Excel export.
        匯出為鄰接矩陣供 Excel 匯出。
        导出为邻接矩阵供 Excel 导出。

        Returns:
            {"nodes": [...], "matrix": [[...]]}
        """
        nodes = list(self.graph.nodes())
        n = len(nodes)
        node_index = {name: i for i, name in enumerate(nodes)}

        matrix = [[0] * n for _ in range(n)]
        for u, v in self.graph.edges():
            i, j = node_index[u], node_index[v]
            matrix[i][j] = 1

        return {"nodes": nodes, "matrix": matrix}

    def get_stats(self) -> dict[str, int]:
        """
        Graph statistics / 圖譜統計 / 图谱统计
        """
        return {
            "node_count": self.graph.number_of_nodes(),
            "edge_count": self.graph.number_of_edges(),
            "components": nx.number_weakly_connected_components(self.graph),
        }

    def to_pptx_data(self) -> dict[str, Any]:
        """
        Prepare data for PPTX visualization.
        準備供 PPTX 視覺化的資料。
        准备供 PPTX 可视化的数据。
        """
        return {
            "stats": self.get_stats(),
            "triples": self.get_triples()[:20],  # Top 20 for slide space
            "top_entities": sorted(
                self.graph.nodes(),
                key=lambda n: self.graph.degree(n),
                reverse=True,
            )[:10],
        }


# --- Demo / 示範 / 示范 ---
if __name__ == "__main__":
    kg = KnowledgeGraphBuilder()

    # Add entities / 新增實體
    kg.add_entity("OpenAI", entity_type="ORG")
    kg.add_entity("GPT-4", entity_type="PRODUCT")
    kg.add_entity("Google", entity_type="ORG")
    kg.add_entity("Gemini", entity_type="PRODUCT")
    kg.add_entity("RAG", entity_type="CONCEPT")

    # Add relations / 新增關係
    kg.add_relation("OpenAI", "developed", "GPT-4")
    kg.add_relation("Google", "developed", "Gemini")
    kg.add_relation("GPT-4", "supports", "RAG")
    kg.add_relation("Gemini", "supports", "RAG")

    print("Stats:", kg.get_stats())
    print("\nTriples:")
    for t in kg.get_triples():
        print(f"  {t['subject']} --{t['predicate']}--> {t['object']}")

    print("\nNeighbors of RAG:")
    for n in kg.get_neighbors("RAG"):
        print(f"  {n['direction']}: {n['entity']} ({n['predicate']})")

    print("\nAdjacency matrix nodes:", kg.to_adjacency_matrix()["nodes"])
