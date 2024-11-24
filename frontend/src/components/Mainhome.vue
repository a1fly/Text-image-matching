<script>
import Header from "@/components/Header.vue";
import Asider from "@/components/Asider.vue";

export default {
  components: {
    Header,
    Asider
  },
  data() {
    return {
      isSidebarCollapsed: true,
    };
  },
  methods: {
    updateStatus(value) {
      this.isSidebarCollapsed = value;
    },
    // 监听窗口大小
    handleResize() {
      this.isSidebarCollapsed = window.innerWidth <= 768;
    },
  },
  mounted() {
    // 初始化窗口大小监听
    window.addEventListener("resize", this.handleResize);
    this.handleResize(); // 初始化检测当前窗口大小
  },
  beforeDestroy() {
    // 移除窗口大小监听器
    window.removeEventListener("resize", this.handleResize);
  },
};
</script>

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
            <img src="../assets/logo2.jpg" alt="不知道放啥" width="110%" height="110%">
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>


<style scoped>
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
  height: 100%; /* 确保主内容区域占满可用高度 */
  background-color: #f5f5f5; /* 添加背景色以便测试 */
}

.center-content {
  text-align: center;
}


/* 布局基础样式 */
#allbox {
  width: 100%;
  height: 100%;
}

#container {
  width: 100%;
  height: 100%;
  background-color: #f5f7fa; /* 整体背景色 */
}


/* 侧边栏样式 */
.el-aside {
  background-color: #ffffff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1); /* 增加侧边栏阴影 */
  overflow: hidden;
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
}

</style>
