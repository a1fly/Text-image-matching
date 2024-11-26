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
        <el-main class="main-content">
          <div class="center-content">

            <el-form
              :model="lostAndFoundForm"
              :rules="rules"
              ref="lostAndFoundForm"
              label-width="120px"
            >
              <!-- 失物描述 -->
              <el-form-item label="失物描述：" prop="description">
                <el-input
                  v-model="lostAndFoundForm.description"
                  placeholder="请输入失物描述"
                ></el-input>
              </el-form-item>

              <!-- 发现地点 -->
              <el-form-item label="发现地点：" prop="location">
                <el-input
                  v-model="lostAndFoundForm.location"
                  placeholder="请输入发现地点"
                ></el-input>
              </el-form-item>



              <!-- 失物照片 -->
              <el-form-item label="失物照片：" prop="lostImage">
                <el-upload
                  action="#"
                  :file-list.sync="lostAndFoundForm.lostImage"
                  list-type="picture"
                  :on-preview="handlePreview"
                  :on-change="handleChange"
                  :auto-upload="false"
                  :on-remove="handleRemove"
                  :limit="1"
                >
                  <el-button size="small" type="primary">上传图片</el-button>
                </el-upload>
              </el-form-item>

              <!-- 处置方式 -->
              <el-form-item label="处置方式：" prop="method">
                <el-radio-group v-model="lostAndFoundForm.method">
                  <el-radio label="1">失物放置在发现地点</el-radio>
                  <el-radio label="2">失主联系我</el-radio>
                  <el-radio label="3">放置在指定地点</el-radio>
                </el-radio-group>
              </el-form-item>

              <!-- 放置地点 -->
              <el-form-item
                v-if="lostAndFoundForm.method === '3'"
                label="放置地点："
                prop="designatedPlace"
              >
                <el-input
                  v-model="lostAndFoundForm.designatedPlace"
                  placeholder="请输入放置地点"
                ></el-input>
              </el-form-item>

              <!-- 放置地点图片上传 -->
              <el-form-item
                v-if="lostAndFoundForm.method === '3'"
                label="地点图片："
                prop="designatedPlaceImage"
              >
                <el-upload
                  action="#"
                  :file-list.sync="lostAndFoundForm.designatedPlaceImage"
                  list-type="picture"
                  :on-preview="handlePreview"
                  :on-change="handleChange"
                  :auto-upload="false"
                  :on-remove="handleRemove"
                  :limit="1"
                >
                  <el-button size="small" type="primary">上传图片</el-button>
                </el-upload>
              </el-form-item>

              <!-- 提交按钮 -->
              <el-form-item>
                <el-button type="primary" @click="onSubmit">提交</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import Asider from "@/components/Asider.vue";

export default {
  components: {
    Header,
    Asider,
  },
  data() {
    return {
      isSidebarCollapsed: true,
      lostAndFoundForm: {
        description: "",
        location: "",
        locationImage: [],
        lostImage: [],
        method: "",
        designatedPlace: "",
        designatedPlaceImage: [],
      },
      rules: {
        description: [{ required: false }],
        location: [{ required: false }],
        lostImage: [
          {
            required: true,
            message: "请上传失物照片",
            trigger: "change",
          },
        ],
        method: [
          {
            required: true,
            message: "请选择处置方式",
            trigger: "change",
          },
        ],
        designatedPlace: [{ required: false }],
      },
    };
  },
  methods: {
    handleRemove(file) {
      console.log("Removed file:", file);
    },
    handlePreview(file) {
      console.log("Preview file:", file);
    },
    handleChange(file, fileList) {
      console.log("Uploaded files:", fileList);
    },
    onSubmit() {
      this.$refs.lostAndFoundForm.validate((valid) => {
        if (valid) {
          console.log("表单提交内容：", this.lostAndFoundForm);
        } else {
          console.error("表单验证失败");
        }
      });
    },
    updateStatus(value) {
      this.isSidebarCollapsed = value;
    },
    handleResize() {
      this.isSidebarCollapsed = window.innerWidth <= 768;
    },
  },
  mounted() {
    window.addEventListener("resize", this.handleResize);
    this.handleResize();
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.handleResize);
  },
};
</script>


<style scoped>
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

#allbox {
  width: 100%;
  height: 100%;
  overflow: auto;
}

#container {
  width: 100%;
  min-height: 100vh; /* 确保容器至少占满整个视口 */
  background-color: #f5f7fa; /* 整体背景色 */
  overflow: auto;
}

.el-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-sizing: border-box;
  background: linear-gradient(to right, #409eff, #66b1ff);
  color: white;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 增加头部阴影 */
}

.main-content {
  display: flex; /* 启用 Flexbox 布局 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */

  min-height: 100%; /* 确保内容区至少占满整个父容器 */
  background-color: #f5f5f5; /* 添加背景色以便测试 */
  overflow-y: auto; /* 启用垂直滚动 */
  padding: 20px; /* 添加内边距 */
}

.center-content {
  text-align: center;
  overflow: auto;
  width: 60%; /* 确保内容区宽度 */
}

/* 侧边栏样式 */
.el-aside {
  background-color: #ffffff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1); /* 增加侧边栏阴影 */
  transition: width 0.3s ease, transform 0.3s ease;
  position: fixed; /* 固定侧边栏，不挤压主内容 */
  height: 100%;
  z-index: 10;
  left: 0;
  border-right: 1px solid #ebeef5; /* 分隔线 */
}

.el-aside.collapsed {
  transform: translateX(-100%);
}

/* 主内容样式 */
.el-main {
  background-color: #ffffff; /* 内容背景色 */
  color: #333;
  text-align: center;
  line-height: 160px;
  padding-left: 250px; /* 为侧边栏留出空间 */
  transition: padding-left 0.3s ease;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1); /* 内容区顶部阴影 */
  border-radius: 10px; /* 内容区圆角 */
}

/* 响应式优化 */
@media (max-width: 768px) {
  .el-main {
    padding-left: 0;
  }
  .center-content {
  width: 100%; /* 确保内容区宽度 */
}

}


</style>
