# 数据目录

本目录被 .gitignore 排除，**高光谱数据一律不放 git**（单景数据动辄几百 MB~几 GB）。

放数据到这里，或在配置/命令里用绝对路径引用服务器其他位置的数据。

建议子目录约定：

```
data/
├── envi/       # ENVI 格式（xxx.hdr + xxx.img）
├── tiff/       # GeoTIFF
└── out/        # agent 工具输出（temp_dir）
```
