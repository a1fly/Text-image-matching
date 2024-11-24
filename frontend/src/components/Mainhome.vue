<script>
export default {
  data() {
    return {
      isSidebarCollapsed: false, // 是否收缩侧边栏
      isMobile: false, // 是否是手机或平板
    };
  },
  methods: {
    // 处理侧边栏选项点击事件
    handleSidebarClick(option) {
      if (option === "lostInfo") {
        alert("填写失物信息功能尚未实现");
      } else if (option === "findLost") {
        alert("寻找失物功能尚未实现");
      } else if (option === "exit") {
        this.$router.push('/login');
      } else if (option === "avatar") {
        alert("头像设置功能尚未实现");
      } else if (option === "contact") {
        alert("联系方式设置功能尚未实现");
      }
    },
    // 监听窗口大小
    handleResize() {
      if (window.innerWidth <= 768) {
        this.isMobile = true;
        this.isSidebarCollapsed = true; // 默认在小屏幕上收起侧边栏
      } else {
        this.isMobile = false;
        this.isSidebarCollapsed = false; // 在大屏幕上始终显示侧边栏
      }
    },
    // 切换侧边栏显示状态
    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
    }
  },
  mounted() {
    // 初始化窗口大小监听
    window.addEventListener("resize", this.handleResize);
    this.handleResize(); // 初始化检测当前窗口大小
  },
  beforeDestroy() {
    // 移除窗口大小监听器
    window.removeEventListener("resize", this.handleResize);
  }
};
</script>

<template>
  <div id="allbox">
    <el-container id="container">
      <!-- 头部 -->
      <el-header height="100px" class="header">
        <div class="header-left">
          <img src="../assets/logo.png" alt="logo" class="logo" />
          <span class="system-name">失物招领系统</span>
        </div>

        <!-- 汉堡图标 -->
        <div v-if="isMobile" class="hamburger" @click="toggleSidebar">
          <i class="el-icon-menu"></i>
        </div>
      </el-header>

      <el-container>
        <!-- 侧边栏 -->
        <el-aside
          class="aside"
          :class="{ collapsed: isSidebarCollapsed }"
          :style="{ width: isSidebarCollapsed ? '0px' : '250px' }"
        >
          <el-menu default-active="1">
            <el-menu-item index="1" @click="handleSidebarClick('lostInfo')">
              <i class="el-icon-edit"></i>
              填写失物信息
            </el-menu-item>
            <el-menu-item index="2" @click="handleSidebarClick('findLost')">
              <i class="el-icon-search"></i>
              寻找失物
            </el-menu-item>

            <!-- 子菜单 -->
            <el-submenu index="3">
              <template #title>
                <i class="el-icon-setting"></i>
                个人设置
              </template>
              <el-menu-item index="3-1" @click="handleSidebarClick('avatar')">
                头像设置
              </el-menu-item>
              <el-menu-item index="3-2" @click="handleSidebarClick('contact')">
                联系方式设置
              </el-menu-item>
            </el-submenu>

            <el-menu-item index="4" @click="handleSidebarClick('exit')">
              <i class="el-icon-switch-button"></i>
              退出登录
            </el-menu-item>
          </el-menu>
        </el-aside>

        <!-- 主内容 -->
        <el-main class="main-content">
          Main 内容
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
/* 布局基础样式 */
#allbox {
  width: 100%;
  height: 100%;
}

#container {
  width: 100%;
  height: 100%;
}

/* 头部样式 */
.el-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-sizing: border-box;
  background: linear-gradient(to right, #66ccff, #0099ff);
  color: white;
  font-weight: bold;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  width: 60px;
  height: 60px;
}

.system-name {
  font-size: 20px;
  margin-left: 10px;
}

/* 汉堡图标 */
.hamburger {
  font-size: 24px;
  cursor: pointer;
  color: white;
}

/* 侧边栏样式 */
.el-aside {
  background-color: #d3dce6;
  overflow: hidden;
  transition: width 0.3s ease, transform 0.3s ease;
  position: fixed; /* 固定侧边栏，不挤压主内容 */
  height: 100%;
  z-index: 10;
  left: 0;
}

.el-aside.collapsed {
  transform: translateX(-100%);
}

.el-menu-item {
  font-size: 16px;
  display: flex;
  align-items: center;
  padding-left: 20px !important;
}

.el-menu-item i {
  margin-right: 10px;
}

.el-menu-item:hover {
  color: #0099ff;
  background-color: #e9eef3;
  cursor: pointer;
}

.el-submenu__title {
  font-size: 16px;
  padding-left: 20px !important;
}

.el-submenu:hover .el-submenu__title {
  color: #0099ff;
}

/* 主内容样式 */
.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: center;
  line-height: 160px;
  padding-left: 250px; /* 为侧边栏留出空间 */
  transition: padding-left 0.3s ease;
}

.main-content {
  padding: 20px;
}

/* 小屏幕调整 */
@media (max-width: 768px) {
  .el-main {
    padding-left: 0; /* 小屏幕时，移除侧边栏的 padding */
  }
}
</style>
