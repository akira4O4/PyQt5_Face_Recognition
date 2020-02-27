import tensorflow as tf

g1 = tf.Graph()
with g1.as_default():
    # 定义变量v，并设置初始值为0
    v = tf.get_variable("v", shape=[2], initializer=tf.zeros_initializer)

g2 = tf.Graph()
with g2.as_default():
    # 定义变量v，并设置初始值为1
    v = tf.get_variable("v", shape=[2], initializer=tf.ones_initializer)

# 在计算图g1中读取变量v的值
with tf.Session(graph=g1) as sess:
    tf.global_variables_initializer().run()
    with tf.variable_scope("", reuse=True):
        print(sess.run(tf.get_variable("v")))

# 在计算图g2中读取变量v的值
with tf.Session(graph=g2) as sess:
    tf.global_variables_initializer().run()
    with tf.variable_scope("", reuse=True):
        print(sess.run(tf.get_variable("v")))

if __name__ == '__main__':
    # 创建图
    a = tf.constant([[1.0, 2.0], [3.0, 4.0]], name="a")
    b = tf.constant([[1.0, 1.0], [0.0, 1.0]], name="b")
    c = tf.matmul(a, b, name='example')
    with tf.Session() as sess:
        print('c.name:',c.name)
        # example:0
        # <name>:0 (0 refers to endpoint which is somewhat redundant)
        # 形如'conv1'是节点名称，而'conv1:0'是张量名称，表示节点的第一个输出张量
        tensor = tf.get_default_graph().get_tensor_by_name("example:0")
        print('tensor:',tensor)
        # Tensor("example:0", shape=(2, 2), dtype=float32)

        all_tensor = tf.get_default_graph().as_graph_def().node
        print('all_tensor:',all_tensor)
