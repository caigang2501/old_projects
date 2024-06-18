import torch
import torch.nn as nn
import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from tqdm import tqdm
from torch.utils.data import DataLoader, Dataset
import os


# 设置超参数
torch.manual_seed(0)
np.random.seed(0)
sequence_length = 8
output = 1
hidden_dim = 256
BATCH_SIZE = 32
NUM_LAYERS = 2
lr = 0.0001
num_epochs = 20
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(device, " version=", torch.__version__)


# 构建位置编码
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
       super(PositionalEncoding, self).__init__()
       pe = torch.zeros(max_len, d_model)
       position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
       div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
       pe[:, 0::2] = torch.sin(position * div_term)
       pe[:, 1::2] = torch.cos(position * div_term)
       pe = pe.unsqueeze(0).transpose(0, 1)
       self.liner = nn.Linear(4, hidden_dim)
       self.register_buffer('pe', pe)

    def forward(self, x):
       return self.liner(x) + self.pe[:x.size(0), :]


# 构建transformer模型
class TransAm(nn.Module):
    def __init__(self, feature_size=hidden_dim, num_layers=NUM_LAYERS, dropout=0.1):
        super(TransAm, self).__init__()
        self.model_type = 'Transformer'
        self.src_mask = None
        self.pos_encoder = PositionalEncoding(feature_size)
        self.encoder_layer = nn.TransformerEncoderLayer(d_model=feature_size, nhead=8, dropout=dropout, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(self.encoder_layer, num_layers=num_layers)
        self.decoder = nn.Linear(feature_size, 1)
        self.init_weights()

    def init_weights(self):
        initrange = 0.1
        self.decoder.bias.data.zero_()
        self.decoder.weight.data.uniform_(-initrange, initrange)

    def forward(self, src):
        # src = (64, 24, 4)
        if self.src_mask is None or self.src_mask.size(0) != len(src):
            device = src.device
            self.src_mask = self._generate_square_subsequent_mask(src.size(1)).to(device)
        # print("src.shape: {}".format(src.shape)) # (64, 24, 4)
        # print("src_mask.shape: {}".format(self.src_mask.shape)) # (24, 24)
        src = self.pos_encoder(src)
        # print("src.shape: {}".format(src.shape)) # (64, 24, hidden_dim)
        output = self.transformer_encoder(src, self.src_mask)
        # print("output.shape: {}".format(output.shape)) # (64, 24, hidden_dim)
        output = output[:, -1].unsqueeze(1)
        # 使用[0, window_size] 预测 []
        # print("output.shape: {}".format(output.shape)) # (64, 1, hidden_dim)
        output = self.decoder(output)
        # print("output.shape: {}".format(output.shape)) # (64, 1, 1)

        return output

    def _generate_square_subsequent_mask(self, sz):
        mask = (torch.triu(torch.ones(sz, sz)) == 1).transpose(0, 1)
        mask = mask.float().masked_fill(mask == 0, float('-inf')).masked_fill(mask == 1, float(0.0))
        
        return mask


# 自己重写数据集继承Dataset
class Mydataset(Dataset):
    def __init__(self, x, y):
        self.x = torch.from_numpy(x)
        self.y = torch.from_numpy(y)

    def __getitem__(self, index):
        x1 = self.x[index]
        y1 = self.y[index]
        return x1, y1

    def __len__(self):
        return len(self.x)


# 读入训练验证和预测数据集
def getData(all_data, sequence_length, batch_size):
    print(all_data.info())
    print(all_data.head().to_string())
    max_price = all_data["price"].max()  # 最大值
    min_price = all_data["price"].min()  # 最小值

    # 训练和验证的数据为第一个点到倒数第六个点的数据
    data = all_data[:-5]
    # 用于预测的数据为最后五个点的数据
    pred_data = all_data[-5:]
    # 删除时间列
    data = data.drop('data', axis=1)
    pred_data = pred_data.drop('data', axis=1)
    print("整理后\n", data.head())
    
    scaler = MinMaxScaler()
    # 对训练验证部分的数据进行(0, 1)标准化
    data = scaler.fit_transform(data)
    # 并根据训练验证数据的范围对需要预测的数据除了price的另外三个维度进行标准化
    pred_data = scaler.transform(pred_data)
    print("训练验证数据维度: {}".format(data.shape))
    print("需要预测的数据维度: {}".format(pred_data.shape))
    
    # 滑动窗口构造 X, Y
    sequence = sequence_length
    # sl = 8, output = 1
    x = []
    y = []
    # 每sl行为一组, 步长为1 (output)
    for i in range(data.shape[0] - sequence):
        x.append(data[i : (i+sequence), :])
        # y为price
        # y.append(df[(i+output) : (i+output+sequence), 0:1])
        y.append(data[(i+sequence) : (i+output+sequence), 0:1])
    x = np.array(x, dtype=np.float32)
    y = np.array(y, dtype=np.float32)

    print("x.shape: {}".format(x.shape))
    print("y.shape: {}".format(y.shape))

    # 构造batch, 构造训练集train与测试集test
    total_len = len(y)
    print("total_len = {}".format(total_len))
    train_x, train_y = x[:-5, ], y[:-5, ]
    # 最后96组作为测试数据
    test_x, test_y = x[-5:, ], y[-5:, ]

    # 创建datalodaer
    print("train_x = {}, train_y = {}".format(train_x.shape, train_y.shape))
    print("test_x = {}, test_y = {}".format(test_x.shape, test_y.shape))
    train_loader = DataLoader(dataset=Mydataset(train_x, train_y), shuffle=True, batch_size=batch_size)
    test_loader = DataLoader(dataset=Mydataset(test_x, test_y), shuffle=False, batch_size=batch_size)
    
    return data, pred_data, max_price, min_price, train_loader, test_loader


model = TransAm().to(device)
criterion = nn.MSELoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 1, gamma=0.95)


# 构建训练函数
def train(train_loader):
    model.train()
    for epoch in range(num_epochs):
        loop = tqdm(enumerate(train_loader), total=len(train_loader))
        for batch_index, i in loop:
            # start_time = time.time()
            total_loss = 0
            data, targets = i
            data, targets = data.to(device), targets.to(device)
            # print("data.shape: {}".format(data.shape)) # (64, 24, 4)
            # print("targets.shape: {}".format(targets.shape))  # (64, 1, 1)
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, targets)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 0.7)
            optimizer.step()
            total_loss += loss.item()
            loop.set_description("epoch:"+str(epoch)+"/"+str(num_epochs))
            loop.set_postfix(loss=loss.item())
    torch.save(model, 'transformer_asfm.pt')


# MAPE和SMAPE
def mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_pred - y_true) / y_true))*100


# 构建验证函数
def evaluate(test_loader, max_price, min_price):
    model = torch.load('transformer_asfm.pt')
    model.eval()
    preds = []
    reals = []
    # labels=[]
    with torch.no_grad():
        for idx, data in enumerate(test_loader):
            x, y = data
            x = x.to(device)
            y = y.to(device)
            pred = model(x)
            # pred: (num_test, 1, 1)
            for i in range(len(pred)):
                preds.append(pred[i][0].item() * (max_price - min_price) + min_price)
                reals.append(y[i][0].item() * (max_price - min_price) + min_price)
    # plt.figure(figsize=(6, 2))
    # plt.plot(preds, label="pred_value")
    # plt.plot(reals, label="real_value", marker='*')
    # plt.legend()
    # plt.savefig("pred_asfm.png", dpi=300)

    MAPE = mape(reals, preds)  # y_test为实际值，y_pre为预测值

    r2 = r2_score(y_true=reals, y_pred=preds)
    # 决定系数，反映的是模型的拟合程度，R2的范围是0到1。
    # 其值越接近1，表明方程的变量对y的解释能力越强，这个模型对数据拟合的也较好。
    print("MAE=", mean_absolute_error(reals, preds))
    print("RMSE=", np.sqrt(mean_squared_error(reals, preds)))
    print("MAPE=", MAPE)
    print("R2=", r2)
    print(preds)
    
    pd.DataFrame(preds).to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_Transformer_test.xlsx'), index=False, header=False)


# 构建预测函数: 自回归预测
def predict(train_data, pred_data, max_price, min_price):
    model = torch.load('transformer_asfm.pt')
    model.eval()
    preds = []
    with torch.no_grad():
        for i in range(len(pred_data)):
            # 预测第1个时, 完全使用训练测试数据中的最后sequence_length个数据
            if i == 0:
                input = train_data[-sequence_length:, ]
            # 预测第sequence_length个之前, 仍需要用到训练测试数据中的最后sequence_length个数据的部分数据
            if i < sequence_length:
                input_1 = train_data[-(sequence_length-i):, ]
                input_2 = pred_data[:i, ]
                input = np.concatenate((input_1, input_2), axis=0)
            # 预测第sequence_length个之后, 只需使用更新后的pred_data中的数据
            if i >= sequence_length:
                input = pred_data[(i-sequence_length): i, ]
            input = torch.tensor(input, dtype=torch.float32).unsqueeze(0)
            # input: (1, sequence_length, 4)
            pred = model(input)[0][0].item()
            # print(pred)
            # 自回归地更新pred_data里每行price的值
            pred_data[i][0] = pred
            # print(pred * (max_price - min_price) + min_price)
            preds.append(pred * (max_price - min_price) + min_price)
    pd.DataFrame(preds).to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_Transformer_pred.xlsx'), index=False, header=False)

def transformer(data_path):
    data = pd.read_excel(data_path, usecols=['data', 'load', 'temperature', 'wind_speed', 'price'])
    train_data, pred_data, max_price, min_price, train_loader, test_loader = getData(
        data, sequence_length=sequence_length, batch_size=BATCH_SIZE)
    print("max_price= {}, min_price = {}".format(max_price, min_price))
    print("len(train_loader) = {}".format(len(train_loader)))
    print("len(test_loader) = {}".format(len(test_loader)))
    train(train_loader)
    evaluate(test_loader, max_price, min_price)
    predict(train_data, pred_data, max_price, min_price)


# transformer("history_50_220107_231110.xlsx")