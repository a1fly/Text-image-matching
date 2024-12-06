<template>
  <div>
    <div
        v-for="(item, index) in iteminfo"
        :key="index"
        class="InfoDisplayframe"
        @click="handleInfoClick(item)"
    >
      <el-image
          style="width: 100px; height: 100px"
          :src="item.imageUrl"
          @click.stop="handleImageClick(item.imageUrl)"
      ></el-image>
      <div class="InfoText">
        <el-descriptions
            class="margin-top"
            size="medium"
            :column="1"
            direction="horizontal">
          <el-descriptions-item>
            <template slot="label">
              <i class="el-icon-document"></i>
              失物描述
            </template>
            <span class="text-ellipsis" :title="item.description">{{ item.description }}</span>
          </el-descriptions-item>

          <el-descriptions-item>
            <template slot="label">
              <i class="el-icon-location-outline"></i>
              发现地点
            </template>
            <span class="text-ellipsis" :title="item.location">{{ item.location }}</span>
          </el-descriptions-item>

          <el-descriptions-item>
            <template slot="label">
              <i class="el-icon-time"></i>
              发现时间
            </template>
            <span class="text-ellipsis" :title="item.findtime">
                    {{ item.findtime[0] }}年
                    {{ item.findtime[1] }}月
                    {{ item.findtime[2] }}日
                    {{ item.findtime[3] }}时
                    {{ item.findtime[4] }}分
                    {{ item.findtime[5] }}秒
                  </span>
          </el-descriptions-item>

        </el-descriptions>
      </div>
    </div>


    <!-- 弹窗展示领取方式 -->
    <el-dialog
        :visible.sync="contactVisible"
        width="40%"
        title="获取方式"
        @close="contactClose"
    >
      <div>
        <el-descriptions size="medium" :column="1" direction="horizontal" border>
          <el-descriptions-item label="领取方式">
            <span>{{ contactmethod }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="联系方式">
            <span v-if="contactmethod === '联系本人'">{{ contact }}</span>
            <span v-else></span>
          </el-descriptions-item>
          <el-descriptions-item label="指定地点">
            <span>{{ designatePlace }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="号码">
            <span v-if="contactmethod === '联系本人'">{{ contactNum }}</span>
            <span v-else></span>
          </el-descriptions-item>

          <el-descriptions-item label="地点图片（可预览）">
            <el-image
                :src="imageSrc"
                :style="{ width: imageWidth, height: imageHeight }"
                @click.stop="handleImageClick(PlaceimageUrl)"
            ></el-image>
          </el-descriptions-item>


        </el-descriptions>
        <el-button id="checkButton" @click="check" type="primary">确认是我的，点击确认领取</el-button>
      </div>
    </el-dialog>

    <!-- 图片预览弹窗 -->
    <el-dialog
        :visible.sync="previewVisible"
        @close="handlePreviewClose"
        :before-close="handlePreviewClose"
    >
      <img
          v-if="previewImage"
          :src="previewImage"
          alt="预览图片"
          style="width: 100%; height: 100%; object-fit: contain;"
      />
    </el-dialog>

  </div>
</template>

<script>

const backimageURL = "http://localhost:5001/static/uploads/";

export default {
  props: {
    iteminfo: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      previewVisible: false,
      contactVisible: false,

      previewImage: '',
      contactmethod: '',
      contact: '',
      contactNum: '',
      designatePlace: '',
      PlaceimageUrl: '',
      findtime: '',
    };
  },
  methods: {
    check() {
      alert("已领取！");
    },
    handleInfoClick(item) {
      console.log("item.PlaceimageUrl:", item.PlaceimageUrl); // 调试信息，查看 PlaceimageUrl
      this.contactmethod = item.contactmethod;
      this.contact = item.contact;
      this.contactNum = item.contactNum;
      this.designatePlace = item.designatePlace;
      this.PlaceimageUrl = item.PlaceimageUrl || ''; // 如果没有 URL，赋值为空字符串
      this.findtime = item.findtime;
      this.contactVisible = true; // 显示对话框
    },
    contactClose() {
      this.contactVisible = false;
    },
    handleImageClick(imageUrl) {
      if (imageUrl === '' || imageUrl === backimageURL) {
        return;
      }
      this.previewImage = imageUrl;
      this.previewVisible = true;
    },
    handlePreviewClose() {
      this.previewVisible = false;
    },
  },
  computed: {
    imageSrc() {
      console.log("进入了imageSrc")
      console.log("this.PlaceimageUrl为 ：", this.PlaceimageUrl)
      return (this.PlaceimageUrl && this.PlaceimageUrl !== backimageURL)
          ? this.PlaceimageUrl
          : require('@/assets/NoPic.jpg');
    },
    imageWidth() {
      return this.PlaceimageUrl && this.PlaceimageUrl !== backimageURL
          ? '100px'
          : '300px';
    },
    imageHeight() {
      return this.PlaceimageUrl && this.PlaceimageUrl !== backimageURL
          ? '100px'
          : '100px';
    }
  },
  mounted() {
  }
};
</script>

<style scoped>
#checkButton {
  background-color: #ff6a00
}

#checkButton:hover {
  background-color: #dfc1ab;
}

#pagechange {
  margin-top: 5%;
}

.InfoText {
  width: 70%;
  max-width: 70%;
  box-sizing: border-box;
  margin-left: 100px;
}

.text-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: inline-block;
  max-width: 100%;
}

.InfoDisplayframe {
  display: flex;
  align-items: center;
  padding: 20px;
  border: 1px solid #f4b34e;
  border-radius: 8px;
  background-color: #ffffff;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-left: auto;
  margin-right: auto;
  width: 60%;
  margin-top: 20px;
}

.InfoDisplayframe:hover {
  border-color: #409eff;
  background-color: #f0f9ff;
  box-shadow: 0 2px 12px rgba(64, 158, 255, 0.3);
}

.el-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-sizing: border-box;
  background: linear-gradient(to right, #804bdd, #6dc9f6);
  color: white;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.main-content {
  background-color: #ffffff;
  color: #333;
  text-align: center;
  line-height: 160px;
  padding: 20px;
  margin-left: auto;
  margin-right: auto;
  width: 60%;
  transition: all 0.3s ease;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.main-content.collapsed {
  width: 80%;
}

.el-aside {
  background-color: #ffffff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: width 0.3s ease, transform 0.3s ease;
  position: fixed;
  height: 100%;
  z-index: 10;
  left: 0;
  border-right: 1px solid #ebeef5;
}

@media (max-width: 768px) {
  .main-content {
    width: 100%;
  }
}
</style>
