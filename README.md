- [Mesh Property](#mesh-property)
  - [1. 计算指定三角Mesh文件的几何属性](#1-计算指定三角mesh文件的几何属性)
  - [用法](#用法)
  - [示例结果](#示例结果)
  - [2. 计算两模型之间的误差距离(METRO | Hausdorff Distance)](#2-计算两模型之间的误差距离metro--hausdorff-distance)
  - [用法](#用法-1)
  - [示例结果](#示例结果-1)
- [Mesh Simplify](#mesh-simplify)
  - [3. 调用PyMeshLab对指定三角mesh模型进行化简](#3-调用pymeshlab对指定三角mesh模型进行化简)
  - [用法](#用法-2)

# Mesh Property

```
python .\mesh_property.py -h
usage: mesh_property.py [-h] -i INPUT [-c COMPARE]

Print mesh properties, logs saved

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input mesh file
  -c COMPARE, --compare COMPARE
                        the compared mesh to get hausdorff distance
```


## 1. 计算指定三角Mesh文件的几何属性
几何属性包含
- 顶点数、边数、面数
- 边界边的数量
- 联通分量数
- 亏格（genus）
- 未使用的顶点数
- 模型是否满足二维流形 2-manifold
  - 非二维流形的顶点数、边数、面数

计算得到的属性信息写入`property_log`文件夹中的log文件，命名格式为`{时间:年月日}_{mesh文件名}.log`

代码见 ``file : mesh_property.py``

## 用法

```
python mesh_property.py -i {mesh file path}

i.e.
python mesh_property.py -i D:\VisualStudioProjects\meshprocessing\result\school\Tile_+004_+007.obj
```

## 示例结果
```
2022-06-13 10:50:50,308 - INFO - Mesh name is Tile_+004_+006.obj
2022-06-13 10:50:50,308 - INFO - vertices_number : 15255 , edges_number : 42139 , faces_number : 26765
2022-06-13 10:50:50,308 - INFO - boundary_edges : 3983
2022-06-13 10:50:50,308 - INFO - connected_components_number : 28
2022-06-13 10:50:50,308 - INFO - genus : 70
2022-06-13 10:50:50,308 - INFO - unreferenced_vertices : 0
2022-06-13 10:50:50,308 - INFO - is_mesh_two_manifold : True
```

## 2. 计算两模型之间的误差距离(METRO | Hausdorff Distance)
以当前模型（I, input mesh）的全部顶点为采样点，统计到比对模型（C, compared mesh）的最近邻顶点的距离
方法参考 `Metro: measuring error on simplified surfaces`
其中主要参考hausdorff distance, 两顶点集的最大化误差

## 用法
```
python .\mesh_property.py -i {sampled_mesh_path} -c {target_mesh_path}

i.e.
python .\mesh_property.py -i D:\VisualStudioProjects\meshprocessing\result\school\Tile_+004_+007.obj -c D:\Mesh\ShanghaiTechRoadModel\Tile_+004_+007\Tile_+004_+007.obj
```

## 示例结果
```
2022-06-13 12:53:32,910 - INFO - Compute hausdorff_distance
2022-06-13 12:53:32,910 - INFO - sampled mesh is D:\VisualStudioProjects\meshprocessing\result\school\Tile_+004_+007.obj
2022-06-13 12:53:32,910 - INFO - target mesh is D:\Mesh\ShanghaiTechRoadModel\Tile_+004_+007\Tile_+004_+007.obj
2022-06-13 12:53:32,911 - INFO - RMS : 0.03880701959133148
2022-06-13 12:53:32,911 - INFO - diag_mesh_0 : 125.16217803955078
2022-06-13 12:53:32,911 - INFO - diag_mesh_1 : 125.1795973451375
2022-06-13 12:53:32,912 - INFO - max : 0.25497397780418396
2022-06-13 12:53:32,912 - INFO - mean : 0.02193104475736618
2022-06-13 12:53:32,912 - INFO - min : 0.0
2022-06-13 12:53:32,912 - INFO - n_samples : 15282
```

# Mesh Simplify
```
python .\mesh_simplify.py -h
usage: mesh_simplify.py [-h] -i INPUT -o OUTPUT [-r RATIO]

Simplify trimesh by MeshLab

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input mesh file
  -o OUTPUT, --output OUTPUT
                        save output filepath, support .obj, .ply
  -r RATIO, --ratio RATIO
                        target percentage
```

## 3. 调用PyMeshLab对指定三角mesh模型进行化简
- pymeshlab是meshlab提供的python接口，用以取代曾经的MeshLab Server, 使得无需打开图形界面，通过命令行调用meshlab
- 化简采用的是QEM(meshing_decimation_quadric_edge_collapse),二次误差度量的边塌缩方法
- 方法不处理颜色材质等信息
- 化简比例 r 为0-1的浮点数, 设输入mesh边数目为$N$, 输出化简后的mesh边数目 $n \leq N \times r$
- 日志信息写入`simplify_logs`文件夹中的log文件，命名格式为`{时间:年月日}_{mesh文件名}.log`

## 用法
```
python -i {input_mesh_path} -o {save_path} -r {simplified ratio}

i.e.
python -i jkroad.obj -o ../result/s01_jkroad.ply -r 0.15 
```
