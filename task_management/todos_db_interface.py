from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TodoNode(Base):
    __tablename__ = "todos"
    # values in the primary_key column must be unique for each row in the table, and you cannot insert a row without providing a value for that column
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, nullable=True)
    description_text = Column(String)


class TodosManager:
    # TODO: add integrate Manager object with creation of TODOs in user interface
    def __init__(self):
        self._engine = create_engine("sqlite:///todos_hierarchy.db")
        Base.metadata.create_all(self._engine)
        Session = sessionmaker(bind=self._engine)
        self._session = Session()
        # Add root node to the hierarchy
        self._root = TodoNode(description_text="root")
        self._session.add(self._root)
        self._session.commit()

    def add_node2hierarchy(self, todo_text: str, parent: TodoNode = None):
        # Add a child node
        if parent is not None:
            child = TodoNode(description_text=todo_text, parent_id=parent.id)
        else:
            # if parent is not specified use root node
            child = TodoNode(description_text=todo_text, parent_id=self._root.id)
        self._session.add(child)
        self._session.commit()

    def get_todo_by_text(self, todo_txt: str):
        todo = self._session.query(TodoNode).filter_by(description_text=todo_txt).first()
        return todo

    def get_todo_by_id(self, todo_txt: str):
        todo = self._session.query(TodoNode).filter_by(id=todo_txt).first()
        return todo

    def query_all_nodes_in_hierarchy(self):
        # Query for all nodes in the hierarchy
        nodes = self._session.query(TodoNode).all()
        for node in nodes:
            print(node.name)
        return nodes


if __name__ == "__main__":
    manager = TodosManager()
    todo_txt = "Go to the toilet"
    manager.add_node2hierarchy(todo_txt)
    manager.get_todo_by_text(todo_txt)
