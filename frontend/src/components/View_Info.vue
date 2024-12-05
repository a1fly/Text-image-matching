<template>
  <div id="allbox">
    <el-container id="container">
      <!-- 头部 -->
      <el-header height="100px" class="header">
        <Header @toggle="updateStatus"></Header>
      </el-header>
      <el-container>
        <!-- 侧边栏 -->
        <el-aside
            class="aside"
            :style="{ width: isSidebarCollapsed ? '0px' : '250px' }"
        >
          <Asider></Asider>
        </el-aside>
        <!-- 主内容 -->
        <el-main
            class="main-content"
            :class="{ collapsed: isSidebarCollapsed }">

          <!-- 动态展示失物信息 -->
          <div
              v-for="(item, index) in items"
              :key="index"
              class="InfoDisplayframe"
              @click="handleInfoClick(item.description, item.location,
              item.contactmethod,item.contact,item.contactNum,item.designatePlace,item.PlaceimageUrl)"
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

          <!-- 分页 -->
          <el-pagination
              id="pagechange"
              :current-page.sync="currentPage"
              :page-size="pageSize"
              layout="prev, pager, next, jumper"
              :total="totalItems"
              @current-change="handlePageChange">
          </el-pagination>

        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import Asider from "@/components/Asider.vue";
import axios from "axios";
const backimageURL="http://localhost:5001/static/uploads/";

export default {
  components: {
    Header,
    Asider
  },
  data() {
    return {
      isSidebarCollapsed: true,
      previewVisible: false, // 控制图片预览对话框的显示与隐藏
      contactVisible: false,

      previewImage: '', // 存储预览的图片 URL
      lostItemDescription: '', // 存储失物描述
      lostItemLocation: '', // 存储失物地点
      contactmethod: '',
      contact: '',
      contactNum: '',
      designatePlace: '',
      PlaceimageUrl: '',
      findtime: '',

      // 分页组件的数据
      currentPage: 1, // 当前页码
      pageSize: 4,    // 每页显示的条目数
      totalItems: 1000, // 总条目数

      items: []
    };
  },
  methods: {
    // 分页组件获取到当前页码
    handlePageChange(newPage) {
      this.currentPage = newPage;
      this.fetchLostItems(this.currentPage, this.pageSize);
      console.log("现在的页数为：", this.currentPage)
    },
    // 确认是否领取
    check() {
      alert("已领取！！！")
      console.log(this.PlaceimageUrl)
      // this.contactVisible =false;
    },

    updateStatus(value) {
      this.isSidebarCollapsed = value;
    },
    // 监听窗口大小
    handleResize() {
      this.isSidebarCollapsed = window.innerWidth <= 768;
    },
    // 点击事件，展示失物信息
    handleInfoClick(description, location, contactmethod,
                    contact, contactNum,
                    designatePlace, PlaceimageUrl, findtime) {
      this.lostItemDescription = description;
      this.lostItemLocation = location;
      this.contactmethod = contactmethod;
      this.contact = contact;
      this.contactNum = contactNum;
      this.designatePlace = designatePlace;
      this.PlaceimageUrl = PlaceimageUrl;
      this.findtime = findtime;


      this.contactVisible = true; // 显示对话框
    },

    handleClaim() {
      this.$message({
        message: "查看领取方式的按钮被点击了！",
        type: "success"
      });

      this.contactVisible = true;

    },
    contactClose() {
      this.contactVisible = false;
    },
    // 图片点击事件
    handleImageClick(imageUrl) {
      if (imageUrl === '' || this.PlaceimageUrl===backimageURL) {
        return;
      }
      console.log("点击图片，图片地址为：", imageUrl)
      this.previewImage = imageUrl;
      this.previewVisible = true;
    },
    // 关闭图片预览对话框
    handlePreviewClose() {
      this.previewVisible = false; // 隐藏图片预览
    },

    // 加载时获取失物数据
    fetchLostItems(page, pageSize) {
      axios.post('api/lost_items', {
        page: page,
        pageSize: pageSize
      })
          .then(response => {
            this.items = response.data.items;
          })
          .catch(error => {
            console.error('Failed to fetch lost items:', error);
          });
    }
  },
  mounted() {
    // 初始化窗口大小监听
    window.addEventListener("resize", this.handleResize);
    this.handleResize(); // 初始化检测当前窗口大小
    this.fetchLostItems(this.currentPage, this.pageSize);
  },
  computed: {
    imageSrc() {
      return this.PlaceimageUrl!==backimageURL || this.PlaceimageUrl=== '' ? this.PlaceimageUrl : require('@/assets/NoPic.jpg');
    },
    imageWidth() {
      return this.PlaceimageUrl!==backimageURL || this.PlaceimageUrl=== '' ? '100px' : '300px';
    },
    imageHeight() {
      return this.PlaceimageUrl!==backimageURL || this.PlaceimageUrl=== ''? '100px' : '100px';
    }
  },
  beforeDestroy() {
    // 移除窗口大小监听器
    window.removeEventListener("resize", this.handleResize);
  },
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
  margin-top: 10px;
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
    width: 90%;
  }
}

#allbox {
  width: 100%;
  height: 100%;
}

#container {
  width: 100%;
  height: 100%;
  background-color: #f5f7fa;
}
</style>
