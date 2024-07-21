import sqlite3
import pandas as pd

class DataBase:
  def __init__(self, db_path):
    self.db_path = db_path
    self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
    self.cursor = self.conn.cursor()
    self.db = None

  def get_table(self, table="source_text", where=None, key="*"):
    if where is None:
      self.df =  pd.read_sql(f"SELECT {key} FROM {table}", self.conn)
    else:
      self.df =  pd.read_sql(f"SELECT {key} FROM {table} WHERE {where}", self.conn)
    return self.df
  
  def close(self):
    self.cursor.close()
    self.conn.close()

  def __del__(self):
    self.close()

class SourceTextDB(DataBase):
  def __init__(self, db_path):
    super().__init__(db_path)
    self.__title = "title"
    self.__level = "level"
    self.__path = "path"
    self.__begin = "beginning"

    self.__create_text_table()
    self.get_table()

  @property
  def title(self):
    return self.__title
  @property
  def level(self):
    return self.__level
  @property
  def path(self):
    return self.__path
  @property
  def begin(self):
    return self.__begin
    
  def __create_text_table(self):
      self.cursor.execute('CREATE TABLE IF NOT EXISTS source_text({} TEXT unique, {} INT, {} TEXT, {} TEXT)'.format(self.title, self.level, self.path, self.begin))

  def __chk_title_existence(self, title):
    self.cursor.execute('select {} from source_text'.format(self.title))
    exists_users = [_[0] for _ in self.cursor]
    if title in exists_users:
      return True
    
  def get_level(self, level):
    df = self.get_table("source_text", f"{self.level}={level}")
    # print("database")
    # print(df)
    return df

  def add_text(self, title, level, source_text):
    if title=="" or level is None or source_text=="":
      return False
    if self.__chk_title_existence(title):
      return False
    begin = " ".join(source_text.split()[:100]) + "..."
    source_path = f"/home/work/data/source_text/{title.replace(' ','_')}.txt"
    with open(source_path, "w") as f:
      f.write(source_text)
    self.cursor.execute('INSERT INTO source_text VALUES(?,?,?,?)', (title, level, source_path, begin))
    self.conn.commit()
    print("追加完了")
    return True
