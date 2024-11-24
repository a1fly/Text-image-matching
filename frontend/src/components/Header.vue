<script>

export default {
  data() {
    return {
      isSidebarCollapsed: false, // 是否收缩侧边栏
      isMobile: false, // 是否是手机或平板
    };
  },
  methods:{
    handleSidebarClick(option) {
      if (option === "lostInfo") {
        alert("填写失物信息功能尚未实现");
      } else if (option === "findLost") {
        alert("寻找失物功能尚未实现");
      } else if (option === "exit") {
        this.$router.push("/login");
      } else if (option === "avatar") {
        alert("头像设置功能尚未实现");
      } else if (option === "contact") {
        alert("联系方式设置功能尚未实现");
      } else if (option === "gohome") {
        this.$router.push("/home");
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
      console.log("isSidebarCollapsed: ", this.isSidebarCollapsed)
      // 发送状态回去给组件
      this.$emit("toggle",this.isSidebarCollapsed)
    },
  }
}
</script>

<template>
  <div class="header">
    <template>

        <div class="header-left">
          <img src="../assets/logo2.jpg" alt="logo" class="logo"/>
          <span class="system-name">智能失物招领</span>
        </div>

        <div class="hamburger" @click="toggleSidebar">
          <i class="el-icon-menu"></i>
        </div>

    </template>
  </div>
</template>

<style scoped>
.header{
 display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  color: white;
  font-weight: bold;
  width: 100%;

}
.header-left {
  display: flex;
  align-items: center;
}
.system-name {
  font-size: 22px;
  margin-left: 15px;
  letter-spacing: 1px;
}

.logo {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 2px solid white;
}

.hamburger {
  font-size: 28px;
  cursor: pointer;
  color: white;
}

</style>