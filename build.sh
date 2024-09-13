echo "清理编译缓存"
rm -rf ./dist 
rm -rf ./build
rm -rf acme_autossl
rm -rf acme_autossl.spec 

echo "开始编译"
echo "开始编译 python 代码..."
pip3 install -r requirement.ini
pyinstaller -F main.py -n acme_autossl
echo "编译python 的代码成功"
echo "开始编译后端代码..."
cd ./web/
yarn install 
yarn build
rm -rf ./www/*
cp -r ./web/dist/* ./www/
echo "后端代码编译成功"
echo "编译结束"

mv ./dist/acme_autossl ./acme_autossl
pkill -9 acme_autossl
rm -rf run.log 
nohup ./acme_autossl > run.log &
echo "重启成功!"

rm -rf ./dist 
rm -rf ./build
rm -rf acme_autossl.spec 
echo "输出实时日志"
tail -n 100 -f run.log 


