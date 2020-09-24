import pymysql
mysqlcon = pymysql.connect("localhost", "root", "root", "u8_test", charset='utf8' )
mysqlcur = mysqlcon.cursor()

from graphviz import Digraph
def plot_model(tree, name):
    g = Digraph("G", filename=name, format='png', strict=False)
    first_label = list(tree.keys())[0]
    g.node("0", first_label,fontname="Microsoft YaHei")
    _sub_plot(g, tree, "0")
    g.view()
root = "0"
def _sub_plot(g, tree, inc):
    global root

    first_label = list(tree.keys())[0]
    ts = tree[first_label]
    for i in ts.keys():
        if isinstance(tree[first_label][i], dict):
            root = str(int(root) + 1)
            g.node(root, list(tree[first_label][i].keys())[0],fontname="Microsoft YaHei")
            g.edge(inc, root, str(i),fontname="Microsoft YaHei")
            _sub_plot(g, tree[first_label][i], root)
        else:
            root = str(int(root) + 1)
            g.node(root, tree[first_label][i],fontname="Microsoft YaHei")
            g.edge(inc, root, str(i),fontname="Microsoft YaHei")

#sql = "select cDepCode,cDepName from xd_u8_003_department order by iDepGrade"
sql = "select deptlevel,name from xd_ehr_department  where deptlevel like \'02%\' order by deptlevel"
mysqlcur.execute(sql)
res = mysqlcur.fetchall()
print(res)
tree = {}
deptmap = dict(res)
for r in res:
    if(len(r[0]) == 2):
        tree.update({r[1]: ""})   #公司级别
    if(len(r[0])==4):
        key = deptmap[r[0][:-2]]
        value = tree[key]
        if(value == ""):  #第一次空
            value = {r[0]:r[1]}
            tree.update({key:value})
        else:
            value.update({r[0]:r[1]})
            tree.update({key:value})
    if(len(r[0]) == 6):
        supdept = r[0][:4]
        dictt = tree[deptmap[r[0][:2]]][supdept]
        if isinstance(dictt, dict):
            dictt[deptmap[supdept]].update({r[0]:r[1]})
        #    dictt.update({deptmap[supdept]:value})
        else:
            tree[deptmap[r[0][:2]]].update({supdept:{dictt:{r[0]:r[1]}}})
    if (len(r[0]) == 8):
        #continue
        supdept = r[0][:6]
        dictt = tree[deptmap[r[0][:2]]] [r[0][:4]] [deptmap[r[0][:4]]] [supdept]
        if isinstance(dictt, dict):
            dictt[deptmap[supdept]].update({r[0]: r[1]})
        else:
            tree[deptmap[r[0][:2]]] [r[0][:4]] [deptmap[r[0][:4]]] .update({supdept: {dictt: {r[0]: r[1]}}})
    if (len(r[0]) == 10):
        #continue
        supdept = r[0][:8]
        dictt = tree[deptmap[r[0][:2]]] [r[0][:4]] [deptmap[r[0][:4]]] [r[0][:6]] [deptmap[r[0][:6]]] [supdept]
        if isinstance(dictt, dict):
            dictt[deptmap[supdept]].update({r[0]: r[1]})
        else:
            tree[deptmap[r[0][:2]]] [r[0][:4]] [deptmap[r[0][:4]]] [r[0][:6]] [deptmap[r[0][:6]]] .update({supdept: {dictt: {r[0]: r[1]}}})

print(tree)
        #print(value)
        #value.update({r[0]:r[1]})
        #tree.update({r[0][:-2] : value})

#print(tree)


d1 = {"no surfacing": {0: "no", 1: {"flippers": {0: "no", 1: "yes"}}}}
d2 = {'tearRate': {'reduced': 'no lenses', 'normal': {'astigmatic': {'yes': {
    'prescript': {'myope': 'hard', 'hyper': {'age': {'young': 'hard', 'presbyopic': 'no lenses', 'pre': 'no lenses'}}}},
    'no': {'age': {'young': 'soft', 'presbyopic': {
        'prescript': {'myope': 'no lenses',
                      'hyper': 'soft'}},
                   'pre': 'soft'}}}}}}

d3 = {"股份总部":{"1":"信息管理","2":{"供应链":{"3":"部门1","4":"部门2"}}}}


#plot_model(d1, "hello.gv")
#plot_model(d2, "hello2.gv")
plot_model(tree,"test3.gv")