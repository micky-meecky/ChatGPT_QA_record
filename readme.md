# ChatGPT Q&A Record


## 1. Introduction

   The purpose of this document is to provide a comprehensive overview of thequestions and answers on the ChatGPT. 
The document is structured as follows: Section 1 provides a summary of the questions and answers.Section 2 provides the specific questions and answers. The document concludes with a list of references used to prepare this summary.

## 2. Q&A


### **Section 1: Questions Index.** 

#### Q1:    为什么会提出self-attention?换句话说，他是怎么来的，是为了解决什么问题来的？
   #### <a name = "Q1"></a>Q2:    self-attetion 的输入是什么，是什么形式的？他的输出又是什么？
   #### Q3:    词向量输入到self-attention之前是不是需要添加该词向量在整个序列中的位置信息？具体又是如何添加的呢？而且除了添加位置信息以外还需要做什么准备嘛？
   #### Q4:    自注意力的过程中，Q，K，V到底如何理解？在计算的时候那几个查询（query）、键（key）和值（value）矩阵的时候，比如计算键矩阵K的时候，K = Wk * ai,(ai为输入词向量)，那个Wk是怎么确定的？时需要在训练过程中自己学习的吗？还是人为设置的？
   #### Q5:    在计算注意力权重，也就是相关性attention score 的时候，除了常用的dot product, 还有一种叫做additive是吗？还有其他方法吗？
   #### Q6:    在自注意力的过程中计算查询矩阵和键矩阵的点积后，那个缩放因子是什么？为什么要除以一个缩放因子？而且后面还跟了个softmax，为什么要有softmax，可以换成relu吗？
   #### Q7:    最后为什么要将注意力权重矩阵与值矩阵相乘，然后再求和得到输入词向量ai对应的bi？
   #### Q8:    self-attention中的self如何理解？
   #### Q9:    多头注意力机制中，如果说现在是词性标注任务，即一个词向量ai对应一个label,bi。此时，对于一个输入序列中的一个词向量a1来说，他通过产生不同的空间表示，产生多个输出向量b11,b12, ... ,b1n, 请问最后怎么将b11,b12, ... ,b1n合成一个最终的a1对应的通过多头注意力模块输出的b1向量呢？
   #### Q10:    为什么要通过一个全连接层将这个矩阵映射到一个新的向量，然后再将这个向量进行归一化得到最终的输出向量b1。具体来说，可以将这个矩阵乘以一个权重矩阵W，并加上一个偏置向量b，然后使用激活函数（比如ReLU）来对结果进行非线性变换呢？
   #### Q11:    你说：“h1 = W[b11; b12; ...; b1n] + b 其中“;”表示向量的连接操作”，请问这里的连接操作通常有哪些？
   #### Q12:    那多头注意力机制的参数量岂不是自注意力机制的参数量的n倍吗？参数量随着头的数量线性增长的，是吗？
   #### Q13:    那多头注意力机制相比于原始自注意力机制的优势在哪里？
   #### Q14:    那在自注意力机制中，我们的那三个矩阵, 也就是查询，键，和值矩阵，在训练过程中初始化的时候是怎么初始化的？那在多头注意力机制中呢？
   #### Q15:    有没有可以用预训练的一些矩阵做特定任务的fine-tuning？
   #### Q16:    multi-label和multi-class的区别是什么?
   #### Q17:    什么是cross attention？
   #### Q18:    什么是teacher facing?
   #### Q19:    请详细解释什么是layer normalization。并解释它与batch normalization的区别以及在transformer中谁更好，以及好的原因。
   #### Q20:    还是不太懂layer normalization， 举个简单的例子说明这个句话吧：”它通过在单个数据样本内，沿着特征维度计算均值和方差，然后对特征进行归一化。”
   


### Section 2: Specific **Q&A** . 

#### [Q1:](#Q1)   为什么会提出self-attention?换句话说，他是怎么来的，是为了解决什么问题来的？


#### A1: 
   I understand that you are asking about the motivation behind the development of self-attention and what problem it was designed to solve. Here's my analysis of your understanding
The concept of self-attention emerged as an attempt to address the limitations of traditional sequence-to-sequence models, like recurrent neural networks (RNNs) and Long Short-Term Memory (LSTM) networks. These models process input sequences sequentially, which can lead to difficulties in capturing long-range dependencies and handling long input sequences.

Self-attention, a core component of the Transformer architecture, was designed to address these issues. It allows the model to weigh the importance of different words or tokens in a sequence with respect to each other, enabling the model to capture long-range dependencies more effectively. The mechanism computes a weighted sum of input representations, with the weights reflecting the relevance of different elements in the sequence.

In summary, self-attention was proposed to tackle the challenges of capturing long-range dependencies and handling long input sequences in traditional sequence-to-sequence models. It enables more efficient and effective processing of input sequences by allowing the model to weigh the importance of different elements in the sequence.


#### Q2:   self-attetion 的输入是什么，是什么形式的？他的输出又是什么？


#### A2: 
   自注意力（self-attention）的输入是一个序列的向量表示，通常是由词嵌入（word embeddings）或其他类型的嵌入表示的。对于一个长度为n的序列，输入矩阵的形状是(n, d)，其中n是序列长度，d是嵌入向量的维度。

自注意力的过程包括以下步骤：

将输入向量投影到三个不同的空间，以计算查询（query）、键（key）和值（value）矩阵。这些矩阵的形状都是(n, d_k)，其中d_k是查询、键和值向量的维度。
计算注意力权重。这是通过计算查询矩阵和键矩阵的点积，然后除以一个缩放因子（通常是d_k的平方根）并应用softmax函数得到的。注意力权重矩阵的形状是(n, n)，表示序列中每个元素与其他元素的相关性。
使用计算得到的注意力权重矩阵与值矩阵相乘。这将得到一个新的表示矩阵，形状为(n, d_k)。
自注意力的输出是一个新的序列表示矩阵，形状为(n, d_k)。这个输出矩阵可以通过其他层（例如前馈神经网络层、归一化层等）进行进一步处理，最终用于解决特定的任务（例如序列到序列任务、分类任务等）。


#### Q3:   词向量输入到self-attention之前是不是需要添加该词向量在整个序列中的位置信息？具体又是如何添加的呢？而且除了添加位置信息以外还需要做什么准备嘛？


#### A3: 
   在将词向量输入到self-attention之前，确实需要添加位置信息。因为Transformer模型并没有像RNN或LSTM那样的内在顺序结构，所以需要额外添加位置信息。位置编码通常通过正弦和余弦函数生成，这些函数的频率和偏移因子变化，使得模型能够捕捉不同位置间的相对关系。位置编码与词向量相加，形成一个新的输入向量。在输入自注意力层之前，不需要其他特殊的准备工作。


#### Q4:   自注意力的过程中，Q，K，V到底如何理解？在计算的时候那几个查询（query）、键（key）和值（value）矩阵的时候，比如计算键矩阵K的时候，K = Wk * ai,(ai为输入词向量)，那个Wk是怎么确定的？时需要在训练过程中自己学习的吗？还是人为设置的？


#### A4: 
   在自注意力过程中，查询（Q）、键（K）和值（V）矩阵是从输入向量中学习的表示。它们通过训练过程中学习的权重矩阵Wq、Wk和Wv进行投影。Wq、Wk和Wv是在训练过程中自动学习的，而不是人为设置的。


#### Q5:   在计算注意力权重，也就是相关性attention score 的时候，除了常用的dot product, 还有一种叫做additive是吗？还有其他方法吗？


#### A5: 
   计算注意力权重时，除了点积（dot product）注意力，还有加法（additive）注意力。加法注意力涉及使用一个权重矩阵将查询和键连接起来，然后通过一个激活函数（如tanh）和另一个权重向量计算分数。除此之外，还有其他注意力机制，如多头注意力（multi-head attention），它将注意力分布在多个表示空间上。


#### Q6:   在自注意力的过程中计算查询矩阵和键矩阵的点积后，那个缩放因子是什么？为什么要除以一个缩放因子？而且后面还跟了个softmax，为什么要有softmax，可以换成relu吗？


#### A6: 
   缩放因子是点积注意力计算过程中的一个调整项。缩放因子通常为d_k的平方根，其中d_k是查询、键和值向量的维度。除以缩放因子有助于防止查询和键向量的点积值过大，导致softmax函数的梯度消失。使用softmax函数是为了将注意力权重归一化到0和1之间，使得它们表示概率分布。将softmax替换为ReLU可能不适用，因为ReLU不会将输出限制在0和1之间，无法提供概率分布。


#### Q7:   最后为什么要将注意力权重矩阵与值矩阵相乘，然后再求和得到输入词向量ai对应的bi？


#### A7: 
   将注意力权重矩阵与值矩阵相乘并求和，是为了根据计算出的权重融合输入序列中的信息。这一步可以将输入词向量中各个位置的信息整合起来，形成新的上下文表示。


#### Q8:   self-attention中的self如何理解？


#### A8: 
   “self”在self-attention中的含义是指在计算注意力权重时，序列中的每个元素都参与计算，包括与自身的关系。这意味着模型不仅关注序列中其他位置的信息，还关注当前位置的信息。这种自我关注机制有助于捕捉序列中长距离和短距离的依赖关系。


#### Q9:   多头注意力机制中，如果说现在是词性标注任务，即一个词向量ai对应一个label,bi。此时，对于一个输入序列中的一个词向量a1来说，他通过产生不同的空间表示，产生多个输出向量b11,b12, ... ,b1n, 请问最后怎么将b11,b12, ... ,b1n合成一个最终的a1对应的通过多头注意力模块输出的b1向量呢？


#### A9: 
   在多头注意力机制中，一个输入向量可以生成多个输出向量，每个输出向量都对应一个不同的注意力头，而最终的输出向量需要将所有头的输出向量合并起来。

具体来说，假设对于一个输入向量a1，多头注意力机制可以生成n个输出向量b11,b12, ... ,b1n，其中每个输出向量都对应一个注意力头。假设每个输出向量的维度都是d，那么可以将这n个输出向量按照注意力头的顺序连接起来，得到一个nd维的向量，即：

[b11; b12; ...; b1n]

其中“;”表示向量的连接操作。这个向量可以被看作是一个n行d列的矩阵，即一个形状为(n, d)的矩阵。

接下来，可以通过一个全连接层将这个矩阵映射到一个新的向量，然后再将这个向量进行归一化得到最终的输出向量b1。具体来说，可以将这个矩阵乘以一个权重矩阵W，并加上一个偏置向量b，然后使用激活函数（比如ReLU）来对结果进行非线性变换，即：

h1 = ReLU(W[b11; b12; ...; b1n] + b)

其中W和b是模型中需要学习的参数，ReLU是一个非线性激活函数。

最后，将h1通过一个softmax函数进行归一化，得到最终的输出向量b1，即：

b1 = softmax(h1)

这样就可以将多头注意力机制中每个注意力头的输出向量合并成一个最终的输出向量，从而完成对输入向量的处理。


#### Q10:   为什么要通过一个全连接层将这个矩阵映射到一个新的向量，然后再将这个向量进行归一化得到最终的输出向量b1。具体来说，可以将这个矩阵乘以一个权重矩阵W，并加上一个偏置向量b，然后使用激活函数（比如ReLU）来对结果进行非线性变换呢？


#### A10: 
   在多头注意力机制中，每个注意力头都会生成一个输出向量，因此会产生多个输出向量，需要将这些输出向量合并成一个最终的输出向量，用于表示输入向量的语义信息。为了将这些输出向量合并起来，并保留每个输出向量的重要信息，通常需要使用一个全连接层对这些向量进行变换和压缩。

具体来说，将多个输出向量按照头的顺序连接成一个矩阵，然后使用一个全连接层来将这个矩阵变换为一个新的向量。这个全连接层可以看作是一种线性变换，将输入的矩阵乘以一个权重矩阵W，再加上一个偏置向量b，即：

h1 = W[b11; b12; ...; b1n] + b

其中“;”表示向量的连接操作。这个向量可以被看作是多个输出向量的拼接，同时也是一个新的向量，它包含了所有头的信息。

为了保留每个输出向量的重要信息，并且在保留这些信息的同时对它们进行压缩，通常会在全连接层之后使用一个非线性激活函数（比如ReLU），对结果进行非线性变换。这个变换可以使得新的向量更加丰富和有意义，同时也能够降低噪声和冗余信息的影响，提高模型的性能。

最后，为了使得输出向量b1的值在0到1之间，并且所有值的和为1，通常会使用softmax函数进行归一化，即：

b1 = softmax(h1)

这样就可以得到一个经过多头注意力机制处理后的最终输出向量b1，用于表示输入向量的语义信息。

#### Q11:   你说：“h1 = W[b11; b12; ...; b1n] + b 其中“;”表示向量的连接操作”，请问这里的连接操作通常有哪些？


#### A11: 
   在向量计算中，连接操作通常有两种方式：垂直连接和水平连接。

垂直连接：将两个向量在竖直方向上按顺序连接起来，得到一个新的向量。通常用“;”或“|”表示，例如：
[a; b]表示将向量a和向量b按垂直方向连接起来。

水平连接：将两个向量在水平方向上按顺序连接起来，得到一个新的向量。通常用“,”或“ ”（空格）表示，例如：
[a, b]表示将向量a和向量b按水平方向连接起来。

在多头注意力机制中，将多个输出向量连接起来，通常使用垂直连接的方式，用“;”来表示向量的连接。这是因为每个输出向量的维度是一样的，通过垂直连接可以将它们按照头的顺序连接成一个矩阵，便于后续的线性变换和非线性变换。

如果假设每个输出向量b11,b12, ... ,b1n都是d维的，那么将它们按照头的顺序进行垂直连接，得到的矩阵的形状就是(n, d)，其中n是注意力头的个数，d是输出向量的维度。

具体来说，将多个输出向量按照头的顺序连接起来，得到一个矩阵B，形状为(n, d)，即：

B = [b11; b12; ...; b1n]

其中“;”表示向量的垂直连接操作，将多个向量按顺序连接成一个矩阵。这个矩阵可以被看作是多个输出向量的集合，其中每一行表示一个输出向量，每一列表示同一个位置上不同头的输出向量。

将这个矩阵乘以一个权重矩阵W，并加上一个偏置向量b，可以将每个输出向量的信息进行变换和压缩，得到一个新的向量h1，即：

h1 = W * B + b

其中W和b是需要学习的参数，用来对多个输出向量进行变换和压缩。最后，对h1进行归一化处理，得到最终的输出向量b1，用于表示输入向量的语义信息。


#### Q12:   那多头注意力机制的参数量岂不是自注意力机制的参数量的n倍吗？参数量随着头的数量线性增长的，是吗？


#### A12: 
   是的，多头注意力机制的参数量确实是自注意力机制的参数量的n倍，其中n是头的数量。

在自注意力机制中，假设输入序列的长度为L，那么需要学习的参数包括查询向量、键向量和值向量的权重矩阵，即三个形状为(d_model, d_model)的权重矩阵，以及一个形状为(d_model,)的偏置向量，总共需要学习的参数量为O(d_model^2)，与序列长度L无关。

而在多头注意力机制中，假设头的数量为n，那么需要学习的参数还包括用于线性变换的n个形状为(d_model, d_model/n)的权重矩阵，以及n个形状为(d_model/n, d_model)的权重矩阵。因此，总共需要学习的参数量为O(n * d_model^2)，与头的数量n成正比。

因此，多头注意力机制的参数量确实随着头的数量线性增长，当头的数量较大时，需要学习的参数数量会急剧增加，这会导致模型的训练和推断时间增加，同时也会增加过拟合的风险。因此，在选择多头注意力机制的头数时，需要在效果和计算成本之间做出平衡。


#### Q13:   那多头注意力机制相比于原始自注意力机制的优势在哪里？


#### A13: 
   多头注意力机制相比于原始自注意力机制的优势主要体现在以下几个方面：

更好的表征能力：多头注意力机制可以生成多个输出向量，每个输出向量都对应一个不同的注意力头，可以捕捉输入序列的不同局部关系，从而更好地表征序列的语义信息。

更好的可解释性：多头注意力机制生成的多个输出向量对应不同的注意力头，可以对模型的预测结果进行可解释性分析，从而更好地理解模型的决策过程。

更好的鲁棒性：多头注意力机制可以并行地处理不同的头，这使得模型更加鲁棒，即使某个头在处理特定的输入时出现了问题，也不会影响其他头的输出结果。

更好的泛化性能：多头注意力机制可以通过学习不同的注意力头，从而更好地适应不同的输入序列和任务场景，具有更好的泛化性能。

总的来说，多头注意力机制可以通过生成多个输出向量，对输入序列的不同部分进行不同程度的关注，从而提高了模型的表征能力、可解释性、鲁棒性和泛化性能，是一种性能更优越的注意力机制。


#### Q14:   那在自注意力机制中，我们的那三个矩阵, 也就是查询，键，和值矩阵，在训练过程中初始化的时候是怎么初始化的？那在多头注意力机制中呢？


#### A14: 
   在自注意力机制中，查询、键和值矩阵的初始化通常采用随机初始化的方式，即使用随机数生成器生成一些服从高斯分布或均匀分布的随机数，并将它们作为权重矩阵的初始值。这些权重矩阵会在模型的训练过程中不断更新，以使得模型可以更好地拟合训练数据。

在多头注意力机制中，除了需要初始化查询、键和值矩阵之外，还需要初始化每个注意力头的权重矩阵。具体来说，每个头都需要学习一个独立的线性变换，这个线性变换可以将输入的查询、键和值进行变换和压缩，从而生成一个新的输出向量。

因此，需要为每个头分别初始化一个查询矩阵、一个键矩阵和一个值矩阵，以及用于线性变换的两个权重矩阵。通常采用与自注意力机制类似的方式进行初始化，即使用随机初始化的方式，生成一些服从高斯分布或均匀分布的随机数，并将它们作为权重矩阵的初始值。这些权重矩阵会在模型的训练过程中不断更新，以使得模型可以更好地拟合训练数据。


#### Q15:   有没有可以用预训练的一些矩阵做特定任务的fine-tuning？


#### A15: 
   是的，可以使用预训练的矩阵进行fine-tuning，以适应特定的任务。

在自然语言处理领域，预训练模型如BERT、GPT等已经取得了很好的效果。这些模型在大规模的文本语料库上进行了预训练，可以学习到一些通用的语义信息，并且可以通过fine-tuning的方式适应特定的任务，例如情感分析、文本分类、问答等。

在fine-tuning过程中，通常会冻结预训练模型中的一些层，只更新与特定任务相关的一些参数。这样可以在不改变预训练模型通用表示能力的基础上，更快地适应特定任务的需求，同时也可以节省训练时间和计算资源。

因此，使用预训练的矩阵进行fine-tuning，是一种有效的方法来提高模型的性能，并且可以在一些具有相似特征的任务之间共享知识，从而提高模型的泛化能力。


#### Q16:   multi-label和multi-class的区别是什么?


#### A16: 
   multi-label和multi-class是分类问题中的两个重要概念，它们的区别如下：

类别数量不同：multi-label分类问题通常有多个标签，每个样本可以属于一个或多个标签；而multi-class分类问题通常只有一个标签，每个样本只能属于一个类别。

输出方式不同：multi-label分类问题的输出通常是一个向量，向量中的每个元素表示样本是否属于某个标签；而multi-class分类问题的输出通常是一个标量，表示样本属于哪个类别。

模型选择不同：在multi-label分类问题中，通常采用一些能够处理多标签输出的模型，例如二元交叉熵损失函数、sigmoid激活函数等；而在multi-class分类问题中，通常采用一些能够处理单一输出的模型，例如softmax分类器、交叉熵损失函数等。

标签相关性不同：在multi-label分类问题中，不同标签之间可能存在相关性，例如一篇文章可能同时包含多个主题；而在multi-class分类问题中，类别之间通常是互斥的，每个样本只能属于其中一个类别。

总的来说，multi-label分类问题和multi-class分类问题的区别在于输出形式、类别数量、模型选择和标签相关性等方面。在实际应用中，需要根据具体的任务和数据集特点选择合适的分类模型和损失函数。


#### Q17:   什么是cross attention？


#### A17: 
   Cross attention（交叉注意力）是一种注意力机制，允许模型在两个不同的序列之间建立关联。在自注意力（self-attention）中，模型关注的是同一个序列内各个元素之间的关系。而在交叉注意力中，模型关注的是两个不同序列中的元素之间的关系。

交叉注意力常用于序列到序列（sequence-to-sequence）任务，如机器翻译、文本摘要等。在这些任务中，模型需要处理输入序列和输出序列。典型的交叉注意力实现是在编码器-解码器（encoder-decoder）架构中。编码器处理输入序列，解码器生成输出序列。

交叉注意力的工作原理如下：

编码器处理输入序列，生成一个表示向量序列。
解码器处理已生成的输出序列（在自回归任务中，通常是生成过程中的历史输出），并计算自注意力。
解码器使用交叉注意力机制关注输入序列的表示。这里，解码器生成的表示充当查询（query），编码器的输出表示充当键（key）和值（value）。
通过计算注意力权重并应用于编码器输出的值（value），解码器获得与输入序列相关的上下文信息。
解码器将这个上下文信息与自注意力信息结合，以生成下一个输出元素。
交叉注意力使模型能够在生成过程中关注输入序列的不同部分，从而更好地捕捉输入和输出之间的依赖关系。


#### Q18:   什么是teacher facing?


#### A18: 
   Teacher forcing是一种训练序列到序列模型的方法。在训练过程中，模型需要预测目标序列。在没有使用teacher forcing的情况下，模型会使用自己预测的输出作为解码器的输入。而使用teacher forcing时，不管模型预测正确与否，都将真实的目标序列作为解码器的输入。这样做可以加速训练过程并提高模型稳定性，但可能导致训练和生成过程的不一致（Exposure Bias）。为解决这个问题，可以采用概率性的teacher forcing，即以一定概率使用真实目标序列作为输入，以一定概率使用模型的预测作为输入。这种策略允许模型在训练过程中逐渐适应自己的预测。


#### Q19:   请详细解释什么是layer normalization。并解释它与batch normalization的区别以及在transformer中谁更好，以及好的原因。


#### A19: 
   Layer normalization（层归一化）是一种归一化技术，用于加速神经网络的训练过程并提高模型的泛化能力。它通过在单个数据样本内，沿着特征维度计算均值和方差，然后对特征进行归一化。具体来说，Layer normalization的计算过程如下：

计算输入特征的均值和方差。
使用均值和方差对输入特征进行归一化。
对归一化后的特征应用缩放因子（scale）和平移因子（shift），这两个因子是可学习的参数。
与Layer normalization相比，Batch normalization（批归一化）也是一种归一化技术，但它是沿着批次维度计算均值和方差。这意味着Batch normalization在一批数据样本中对每个特征进行归一化。Batch normalization在卷积神经网络（CNN）中应用广泛，因为它能够有效地处理批次间的协方差偏移。

在Transformer模型中，Layer normalization更为常用，原因如下：

序列长度可变：在自然语言处理任务中，输入序列的长度可能不同。Layer normalization可以在单个样本内独立处理每个特征，适应不同长度的序列。而Batch normalization需要固定批次大小和序列长度，处理可变长度序列时可能会遇到问题。

解码器的自回归生成：在Transformer解码器中，输出序列是逐步生成的。在生成过程中，Batch normalization需要同时处理多个输出，但自回归生成只有一个输出。Layer normalization适用于这种情况，因为它在单个样本内进行归一化。

独立于批次大小：Layer normalization在单个数据样本内进行归一化，与批次大小无关。这使得模型在不同批次大小下的表现更为稳定。而Batch normalization在不同批次大小下的性能可能会受到影响。

综上，Layer normalization在Transformer模型中更为常用，因为它适应可变长度序列、支持自回归生成过程，并且在不同批次大小下的表现更稳定。


#### Q20:   还是不太懂layer normalization， 举个简单的例子说明这个句话吧：”它通过在单个数据样本内，沿着特征维度计算均值和方差，然后对特征进行归一化。”


#### A20: 
   当然，让我们用一个简单的例子来解释Layer normalization。假设我们有一个单层神经网络，输入特征向量 x = [x1, x2, x3]，经过神经网络后得到输出特征向量 y = [y1, y2, y3]。注意这里我们只有一个数据样本。

对于Layer normalization，我们关注的是在单个数据样本内（即输出向量y）沿着特征维度（在这个例子中是y1, y2, y3）进行归一化。首先，我们计算特征的均值和方差：

均值 μ = (y1 + y2 + y3) / 3
方差 σ2 = ((y1 - μ)2 + (y2 - μ)2 + (y3 - μ)2) / 3

然后，我们用这个均值和方差对特征向量 y 进行归一化：

y_normalized = [(y1 - μ) / sqrt(σ2 + ε), (y2 - μ) / sqrt(σ2 + ε), (y3 - μ) / sqrt(σ2 + ε)]

这里的ε（epsilon）是一个很小的数，用来防止除数为零。

最后，我们使用可学习的缩放因子（scale）γ和平移因子（shift）β来对归一化后的特征进行缩放和平移：

y_final = [γ1 * y_normalized1 + β1, γ2 * y_normalized2 + β2, γ3 * y_normalized3 + β3]

在训练过程中，γ和β是可学习的参数，可以通过梯度下降法进行优化。

这个例子展示了如何在单个数据样本内，沿着特征维度进行Layer normalization。在实际应用中，神经网络可能有更多层和更多维度的特征，但Layer normalization的基本概念和计算方法与此例子相同。


