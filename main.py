# 필요한 라이브러리 import
import numpy as np  # numpy 추가
from log_collector import LogCollector
from anomaly_detector import AnomalyDetector
from response_handler import ResponseHandler

def main_pipeline():
    # Step 1: 로그 수집 및 저장
    collector = LogCollector()
    collector.send_logs()
    collector.consume_and_store_logs()

    # Step 2: 이상 탐지
    detector = AnomalyDetector()

    # 정형 데이터 샘플
    structured_data = np.array([
        [10, 1], [12, 2], [15, 3], [100, 50]  # 마지막 데이터는 이상치
    ])
    lstm_results = detector.detect_with_lstm(structured_data)
    print("LSTM Anomaly Detection Results:", lstm_results)

    # 비정형 데이터 샘플
    unstructured_logs = [
        "System started successfully.",
        "Failed to connect to database.",
        "Disk usage is above 80%."
    ]
    bert_results = detector.detect_with_bert(unstructured_logs)
    print("BERT Anomaly Detection Results:", bert_results)

    # Step 3: 자동 대응
    handler = ResponseHandler()
    for i, result in enumerate(bert_results):
        if result == "Anomaly":
            log_message = unstructured_logs[i]
            print(f"Anomaly detected in log: {log_message}")
            handler.send_slack_alert(f"Anomaly detected: {log_message}")
            handler.trigger_soar_playbook(f"Anomaly details: {log_message}")

if __name__ == "__main__":
    main_pipeline()