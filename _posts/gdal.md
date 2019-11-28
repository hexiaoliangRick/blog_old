# GDAL 学习记录

###链接
1.GDAL源码下载地址  https://trac.osgeo.org/gdal/wiki/DownloadSource   
2.pro4j 文档地址 https://proj.org/install.html#windows   
3.OSGeo4w 地址 https://trac.osgeo.org/osgeo4w/


## 环境搭建
###1.win10  idea java 如何搭建GDAL的开发环境：
####  手动编译gdal 2.3.2   
    -------
    参考文章：
    源码到java应用 https://blog.csdn.net/lw19910913/article/details/77746164
    GDAL编译   https://blog.csdn.net/qq_32153213/article/details/81363588
    GDAL代码例子：https://www.programcreek.com/java-api-examples/?api=org.gdal.gdal.Dataset  
    
    --------  
    1.安装必要的软件:         
        - JDK  ```http://www.oracle.com/technetwork/java/javase/downloads/index.html```      
        - Ant   类似Maven的包管理工具```http://ant.apache.org/bindownload.cgi```   【下载解压，无需安装】   
        - swig  接口扩展工具，生成多种语言的接口调用工具```​http://www.swig.org/download.html```   【下载解压，无需安装】   
                    
    2.修改编译配置文件   
        - gdal编译相关配置  
            1. 57行 GDAL_HOME 控制编译后的gdal输出目录，如果系统环境变量设置了该值，最后以系统环境变量的为准
            2. 187行 WIN64 修改为 WIN64=YES  ，控制32位或者64位
        - java调用接口相关配置    
            1. 86行 SWIG 修改为前一步文件夹   
            2. 91行 JAVA_HOME    
            3. 94行 ANT_HOME          
    3.编译  
    - 编译GDAL   
        1.cd 至源码文件夹  
        2.nmake /f makefile.vc    
        3.nmake /f makefile.vc install    
        4.nmake /f makefile.vc devinstall  
    - 编译 Java调用相关
        1.  cd 至源代码文件夹下的swig文件夹下   
        2.   nmake /f makefile.vc java   
        3.  查看编译结果 ：/swig/java目录下为编译的结果   
        
        
#### vs2015 win10 gdal 3.0.2 手动编译


#### OSGeo4w 简介和使用方法
 

#### 引入gdal 问题   
    1.将gdal文件添加至系统环境变量中  
    2.在工程目录下简历lib文件夹，将gdal.jar 放入该目录，添加对该jar文件的pom引用。
## Raster  
## Vector  