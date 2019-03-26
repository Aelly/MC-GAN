mkdir -p ./checkpoints/GlyphNet_pretrain

MODEL_FILE=./checkpoints/GlyphNet_pretrain/200_net_G.pth
URL=download1644.mediafire.com/urtb4u11rpmg/03bsjb5u8au95uh/200_net_G.pth
wget -N $URL -O $MODEL_FILE

MODEL_FILE=./checkpoints/GlyphNet_pretrain/200_net_G_3d.pth
URL=http://download1485.mediafire.com/xahox28c55ng/zo7srld08tuol5q/200_net_G_3d.pth
wget -N $URL -O $MODEL_FILE
