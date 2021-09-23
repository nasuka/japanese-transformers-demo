import json
import os
from typing import Any, Dict

import pandas as pd
import requests
import streamlit as st

from logger import get_module_logger

LOGGER = get_module_logger(__name__)
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
HUGGINGFACE_API_URL = (
    "https://api-inference.huggingface.co/models/joeddav/xlm-roberta-large-xnli"
)


@st.cache
def query_inference_api(request_body: Dict[str, Any]) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    data = json.dumps(request_body)
    response = requests.request("POST", HUGGINGFACE_API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


def build_predction_df(pred: Dict[str, Any]) -> pd.DataFrame:
    df = pd.DataFrame()
    df["label"] = pred["labels"]
    df["score"] = pred["scores"]
    return df


def main() -> None:
    st.set_page_config(
        page_title="Zero Shot Classification",
    )
    st.markdown("# Zero-Shot Text Classification Demo")

    text = st.text_area(
        "please input text",
        "明示的な指示を用いることなく、その代わりにパターンと推論に依存して、特定の課題を効率的に実行するためにコンピュータシステムが使用するアルゴリズムおよび統計モデルの科学研究",
    )
    label_text = st.text_input(
        "please input label text(separated by comma)", "機械学習, 機械工学, 物理学, 化学, 社会工学"
    )
    labels = label_text.replace("、", ",").split(",")

    if text:
        # predict labels
        request_body = {"inputs": text, "parameters": {"candidate_labels": labels}}
        pred = query_inference_api(request_body)
        LOGGER.info("prediction: ", pred)
        pred_label = pred["labels"][0]

        # display prediction result
        st.markdown(f"text: {text}")
        st.markdown(f"label: **{pred_label}**")
        pred_df = build_predction_df(pred)
        st.table(pred_df)

        LOGGER.info(
            {
                "text": text,
                "labels": label_text,
                "predicted_label": pred_label,
            }
        )

    st.markdown("hosted by [@naohachi89](https://twitter.com/naohachi89)")


if __name__ == "__main__":
    main()
