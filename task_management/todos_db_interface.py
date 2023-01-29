from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TodoNode(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, nullable=True)
    name = Column(String)


class TodosManager:

    def __init__(self):
        self._engine = create_engine("sqlite:///todos_hierarchy.db")
        Base.metadata.create_all(self._engine)
        Session = sessionmaker(bind=self._engine)
        self._session = Session()
        # Add root node to the hierarchy
        self._root = TodoNode(name="root")
        self._session.add(self._root)

    def add_node2hierarchy(self, todo_text: str, parent: TodoNode = None):
        # Add a child node
        if parent is not None:
            child = TodoNode(name=todo_text, parent_id=parent.id)
        else:
            # if parent is not specified use root node
            child = TodoNode(name=todo_text, parent_id=self._root.id)
        self._session.add(child)

    def commit_session(self):
        self._session.commit()

    def query_all_nodes_in_hierarchy(self):
        # Query for all nodes in the hierarchy
        nodes = self._session.query(TodoNode).all()
        for node in nodes:
            print(node.name)
        return nodes


if __name__ == "__main__":
    manager = TodosManager()
    manager.add_node2hierarchy("Go to the toilet")
