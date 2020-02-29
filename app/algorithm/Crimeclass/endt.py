# 罪名预测模型生成程序
# coding=utf-8
import os
from multiprocessing import cpu_count
import numpy as np
import paddle
import paddle.fluid as fluid
import io
gpu
class classify():
    data_root_path = ""
    # 字典所在的路径和文件
    dict_path="/home/aistudio/data/dans.txt"
    # 模型生成后存放的路径及文件名
    model_save_dir = "/home/aistudio/work/feileiqi/"
    save_path = '/home/aistudio/data/result.txt'
    # 训练数据集所在的路径及文件名(已经向量化好的文件，前面是向量，最后一项是类别标号）
    train_data_path="/home/aistudio/data/trainresult.txt"
    # 验证数据集所在的路径及文件名(已经向量化好的文件，前面是向量，最后一项是类别标号）
    val_data_path="/home/aistudio/data/testresult.txt"
        
    @staticmethod
    def train(self):
        #
        # 获取字典长度
        def get_dict_len(d_path):
            with io.open(d_path, 'r', encoding='utf-8') as f:
                 line = eval(f.readlines()[0])

            return len(line.keys())
         
       
    # 创建数据读取器train_reader 和test_reader
    # 训练/测试数据的预处理
        def data_mapper(sample):
            data, label = sample
            data = [int(data) for data in data.split(',')]
            return data, int(label)

    # 创建数据读取器train_reader
        def train_reader(train_list_path):
            def reader():
                with open(train_list_path, 'r') as f:
                     lines = f.readlines()
                     # 开始读取每句话和标签
                     for line in lines:
                         data, label = line.split('\t')
                         yield data, label
            return paddle.reader.xmap_readers(data_mapper, reader, cpu_count(), 1024)
    #  创建数据读取器test_reader
        def test_reader(test_list_path):
            def reader():
                with open(test_list_path, 'r') as f:
                     lines = f.readlines()
                     for line in lines:
                         data, label = line.split('\t')
                         yield data, label

            return paddle.reader.xmap_readers(data_mapper, reader, cpu_count(), 1024)
        
        
        # 创建CNN网络
        # CNN函数的参数中clss_dim是类别数目，emb_dim是输入层的维度，hid是卷积层的维度
        def CNN_net(data,dict_dim, class_dim=65, emb_dim=128, hid_dim=128,hid_dim2=64):
            emb = fluid.layers.embedding(input=data,size=[dict_dim, emb_dim])
            conv_3 = fluid.nets.sequence_conv_pool(
                                                 input=emb,
                                                 num_filters=hid_dim,
                                                 filter_size=3,
                                                 act="relu",
                                                 pool_type="sqrt")
            conv_4 = fluid.nets.sequence_conv_pool(
                                                 input=emb,
                                                 num_filters=hid_dim2,
                                                 filter_size=4,
                                                 act="relu",
                                                 pool_type="sqrt")
                                                 
            output = fluid.layers.fc(input=[conv_3, conv_4], size=class_dim, act='softmax')
            return output
           
         # 定义输入数据， lod_level不为0指定输入数据为序列数据
        words = fluid.layers.data(name='words', shape=[1], dtype='int64', lod_level=1)
        label = fluid.layers.data(name='label', shape=[1], dtype='int64')
     
         # 获取数据字典长度
        dict_dim = get_dict_len(self.dict_path)
        
        #print('dict_dim:%d'%(dict_dim))
     
         # 获取卷积神经网络  # 获取分类器
        model = CNN_net(words, dict_dim)
     
         # 获取损失函数和准确率
        cost = fluid.layers.cross_entropy(input=model, label=label)
        avg_cost = fluid.layers.mean(cost)
        acc = fluid.layers.accuracy(input=model, label=label)

         # 获取预测程序
        test_program = fluid.default_main_program().clone(for_test=True)

         # 定义优化方法
        optimizer = fluid.optimizer.AdamOptimizer(learning_rate=0.0016)
        opt = optimizer.minimize(avg_cost)
     
         # 创建一个执行器，CPU训练速度比较慢，选择用GPU计算
        place = fluid.CUDAPlace(0)
        exe = fluid.Executor(place)
         # 进行参数初始化
        exe.run(fluid.default_startup_program())
     
         # 获取训练数据读取器和测试数据读取器
        train_reader = paddle.batch(reader=train_reader(self.train_data_path), batch_size=100)
        test_reader = paddle.batch(reader=test_reader(self.val_data_path), batch_size=100)
     
         # 定义数据映射器
        feeder = fluid.DataFeeder(place=place, feed_list=[words, label])
     
        EPOCH_NUM=15
        # 开始训练

        for pass_id in range(EPOCH_NUM):
         # 进行训练
            for batch_id, data in enumerate(train_reader()):
                train_cost, train_acc = exe.run(program=fluid.default_main_program(),
                                  feed=feeder.feed(data),
                                  fetch_list=[avg_cost, acc])

                if batch_id % 500 == 0:
                    print('Pass:%d, Batch:%d, Cost:%0.5f, Acc:%0.5f' % (pass_id, batch_id, train_cost[0], train_acc[0]))
    
        # 进行测试
        test_costs = []
        test_accs = []
        for batch_id, data in enumerate(test_reader()):
            test_cost, test_acc = exe.run(program=test_program,
                                              feed=feeder.feed(data),
                                              fetch_list=[avg_cost, acc])
            test_costs.append(test_cost[0])
            test_accs.append(test_acc[0])

        # 计算平均预测损失在和准确率
        test_cost = (sum(test_costs) / len(test_costs))
        test_acc = (sum(test_accs) / len(test_accs))
        print('Test:%d, Cost:%0.5f, ACC:%0.5f' % (pass_id, test_cost, test_acc))

        # 保存预测模型
        if not os.path.exists(self.model_save_dir): 
            os.makedirs(self.model_save_dir) 
            fluid.io.save_inference_model(self.model_save_dir,feeded_var_names=[words.name], target_vars=[model], executor=exe)

        
        print('训练模型保存完成！')
        #self.test(self)
        
            
if __name__ == "__main__":
    classify.train(classify)
