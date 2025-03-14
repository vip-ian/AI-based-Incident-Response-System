import torch
import torch.nn as nn
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification

class AnomalyDetector:
    def __init__(self):
        pass

    def detect_with_lstm(self, data):
        class LSTMModel(nn.Module):
            def __init__(self, input_size, hidden_size, num_layers, output_size):
                super(LSTMModel, self).__init__()
                self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
                self.fc = nn.Linear(hidden_size, output_size)

            def forward(self, x):
                out, _ = self.lstm(x)
                out = self.fc(out[:, -1, :])  # 마지막 시점 출력
                return out

        X = torch.tensor(data, dtype=torch.float32).unsqueeze(0)  # 배치 차원 추가
        model = LSTMModel(input_size=2, hidden_size=50, num_layers=2, output_size=1)
        model.eval()  # 평가 모드
        with torch.no_grad():
            predictions = model(X)
            anomalies = (predictions > 0.5).int()  # 임계값 기반 이상 감지
            return anomalies.numpy()

    def detect_with_bert(self, logs):
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
        results = []
        for log in logs:
            inputs = tokenizer(log, return_tensors="pt", truncation=True, padding=True)
            outputs = model(**inputs)
            prediction = torch.argmax(outputs.logits, dim=-1).item()
            results.append("Anomaly" if prediction == 1 else "Normal")
        return results