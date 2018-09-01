#! /bin/bash

#把当前目录下图片重命名(删除空格和括号)，把图片文件名封装为列表存入py文件中。

STATIC_DIR=$(cd $(dirname $BASH_SOURCE); pwd)
ITNEWS_DIR=$(cd ${STATIC_DIR}/../Itnews; pwd)
#ITNEWS_DIR=${STATIC_DIR}/../Itnews

cd $STATIC_DIR

for i in *.jpg *.png
do
	PIC=""
	if [[ "$i" =~ "(" ]] || [[ "$i" =~ ")" ]]
	then
		PIC=$(echo $i | sed 's/(//g')
		PIC=$(echo $PIC | sed 's/)//g')
		mv "$i" $PIC
		#echo $i
	fi
done

for i in *.jpg *.png
do
	PIC=""
	if [[ "$i" =~ " " ]]
	then
		for j in $i
		do
			PIC="${PIC}${j}"
		done
		mv "$i" $PIC
	fi
done


echo "piclist = [" > picture_list.py
for i in *.jpg *.png
do
	echo "    \"${i}\"," >> picture_list.py
done
echo "]" >> picture_list.py

mv $STATIC_DIR/picture_list.py $ITNEWS_DIR/
