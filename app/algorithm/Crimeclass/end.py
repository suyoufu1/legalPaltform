# coding=utf-8
#用训练好的模型进行预测并输出预测结果
#创建执行器
import sys
import json
import os
import io
from multiprocessing import cpu_count
import numpy as np
from collections import OrderedDict
import shutil
import paddle
import paddle.fluid as fluid
place=fluid.CPUPlace()
exe = fluid.Executor(place)
infer_exe=fluid.CPUPlace()
infer_exe=fluid.Executor(place)
infer_exe.run(fluid.default_startup_program())
# G:\pythonWeb\pythons\end\fenleiqi
save_path=r'C:\Users\Administrator\PycharmProjects\legalPlatform\app\algorithm\Crimeclass\fenleiqi'
#从模型中获取预测程序，输入数据名称列表、分类器
[infer_program,feeded_var_names,target_var]=fluid.io.load_inference_model(dirname=save_path,executor=infer_exe)
'''
def encoder(is_sparse):
    src_word_id = pd.data(
     name="src_word_id", shape=[1], dtype='int64', lod_level=1)
    src_embedding = pd.embedding(
     input=src_word_id,
     size=[dict_size, word_dim],
     dtype='float32',
     is_sparse=is_sparse,
     param_attr=fluid.ParamAttr(name='vemb'))

    fc1 = pd.fc(input=src_embedding, size=hidden_dim * 4, act='tanh')
    lstm_hidden0, lstm_0 = pd.dynamic_lstm(input=fc1, size=hidden_dim * 4)
    encoder_out = pd.sequence_last_step(input=lstm_hidden0)
    return encoder_out
'''


#获取数据
def get_data(sentence):
      #读取数据字典
      with io.open(r'C:\Users\Administrator\PycharmProjects\legalPlatform\app\algorithm\Crimeclass\dans.txt','r',encoding='utf-8') as f_data:
            # print(f_data.readline())
            dic_txt=json.loads(f_data.readline())
      
      #把字符串数据转换成列表数据
      # print(dic_txt)
      keys=dic_txt.keys()
     
      data1=[]
      if len(sentence) == 0 or sentence == None:
            return ""
      for s in sentence:
            #判断是否存在未知字符
            if not s in keys:
                  s='<unk>'
                  data1.append(np.int64(dic_txt[s]))
            else:
                  data1.append(np.int64(dic_txt[s]))

      #获取图片数据
      #data1=get_data(sys.argv[1])
      # data2=get_data('有人杀人')
      # data.append(data2)
      print(data1)
      data = []
      data.append(data1)
      #获取每句话的单词数量
      base_shape=[[len(c) for c in data]]
      print(base_shape)
      #生成预测数据
      tensor_words=fluid.create_lod_tensor(data,base_shape,place)
      print(tensor_words)
      #执行预测
      result=exe.run(program=infer_program,
            feed={feeded_var_names[0]:tensor_words},
            fetch_list=target_var
            )
      print(result)
      #分类名称
      name = {}
      with open(r'C:\Users\Administrator\PycharmProjects\legalPlatform\app\algorithm\Crimeclass\zuimings.txt', 'r', encoding='utf-8') as f:
                  name = json.loads(f.readline(),object_pairs_hook=OrderedDict)
      n = name
      print(type(n))
      print(n)
      mynames=n.keys()
      names=[]
      for key in n.keys():
            names.append(key)
      #过去数据概率最大的lable
      lab = 0
      for i in range(len(data)):
            lab=np.argsort(result)[0][i][-1]
            print(np.argsort(result)[0][i])
            print(lab)
            print(names[lab])
            print('预测结果为: %d, 名称为: %s, 概率为: %f'%(lab,names[lab],result[0][i][lab]))
      print(lab)
      return names[lab]
# get_data("")