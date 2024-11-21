import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# SQLAlchemyのセットアップ
DATABASE_URL = "sqlite:///records.db"  # SQLiteファイルのパス
Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# データベースのモデル
class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    action = Column(String, nullable=False)
    details = Column(String)

# テーブル作成
Base.metadata.create_all(bind=engine)

# Streamlitアプリ
st.title("役に立つ行動記録アプリ")

# セッションを作成
session = SessionLocal()

# ユーザー入力
date = st.date_input("日付を選択", value=datetime.today())
action = st.text_input("今日の行動")
details = st.text_area("詳細を書く")

if st.button("記録を保存"):
    new_record = Record(date=date, action=action, details=details)
    session.add(new_record)
    session.commit()
    st.success("記録が保存されました！")

# 過去の記録を表示
st.subheader("過去の記録")
records = session.query(Record).order_by(Record.date.desc()).all()
df = pd.DataFrame([{"Date": r.date, "Action": r.action, "Details": r.details} for r in records])
st.dataframe(df)
