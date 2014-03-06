def adj_w(node, err_o, w_no):
    err_n = node * (1 - node) * (err_o * w_no)
    w_no += l*err_o*node
    return (err_n, w_no)

o_1 = 1.0
o_2 = 2.0
w_13 = -3
w_14 = 2
w_15 = 4
w_23 = 2
w_24 = -3
w_25 = 0.5
w_36 = 0.2
w_46 = 0.7
w_56 = 1.5
o_3 = 0.7311
o_4 = 0.0179
o_5 = 0.9933
err_6 = -0.11346127339699999
err_5 = -0.0011326458827956695
w_56 = 0.37298917134759924
l = 10

err_4 = adj_w(o_4, err_6, w_46)[0]
err_3 = adj_w(o_3, err_6, w_36)[0]
w_46 = adj_w(o_4, err_6, w_46)[1]
w_36 = adj_w(o_3, err_6, w_36)[1]
w_25 = adj_w(o_2, err_5, w_25)[1]
w_24 = adj_w(o_2, err_4, w_24)[1]
w_23 = adj_w(o_2, err_3, w_23)[1]
w_15 = adj_w(o_1, err_5, w_15)[1]
w_14 = adj_w(o_1, err_4, w_14)[1]
w_13 = adj_w(o_1, err_3, w_13)[1]
print err_4
print err_3
print w_46
print w_36
print w_25
print w_24
print w_23
print w_15
print w_14
print w_13