<template>
  <div class="asideritem">
    <template>
      <el-menu default-active="1">
        <el-menu-item index="1" @click="handleSidebarClick('gohome')">
          <i class="el-icon-house"></i>
          <span slot="title">首页</span>
        </el-menu-item>
        <el-menu-item index="2" @click="handleSidebarClick('lostInfo')">
          <i class="el-icon-upload"></i>
          <span slot="title">填写失物信息</span>
        </el-menu-item>
        <el-menu-item index="3" @click="handleSidebarClick('findLost')">
          <i class="el-icon-search"></i>
          <span slot="title">寻找失物</span>
        </el-menu-item>

        <!-- 子菜单 -->
        <el-submenu index="4">
          <template #title>
            <i class="el-icon-setting"></i>
            <span>个人设置</span>
          </template>
          <el-menu-item index="4-1" @click="handleSidebarClick('avatar')">
            头像设置
          </el-menu-item>
          <el-menu-item index="4-2" @click="handleSidebarClick('contact')">
            联系方式设置
          </el-menu-item>
        </el-submenu>

        <el-menu-item index="5" @click="handleSidebarClick('exit')">
          <i class="el-icon-switch-button"></i>
          <span slot="title">退出登录</span>
        </el-menu-item>
      </el-menu>
    </template>

  </div>
</template>

<script>
export default {

  methods: {
    handleSidebarClick(route) {
      // 处理点击事件
      console.log(`点击了 to ${route}`);
      if (route === 'gohome' && this.$route.path !== '/home') {
        this.$router.push('/home');
      } else if (route === 'lostInfo' && this.$route.path !== '/write') {
        this.$router.push('/write');
      } else if (route === 'findLost' && this.$route.path !== '/findLost') {
        this.$router.push('/findLost');
      } else if (route === 'avatar' && this.$route.path !== '/avatar') {
        this.$router.push('/avatar');
      } else if (route === 'contact' && this.$route.path !== '/contact') {
        this.$router.push('/contact');
      } else if (route === 'exit' ) {
        this.$router.push('/login');
      }

    }
  }
};
</script>

<style scoped>
.asider {
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

.asider.collapsed {
  width: 64px; /* 收起时的宽度 */
}

.el-menu-item {
  font-size: 16px;
  display: flex;
  align-items: center;
  padding-left: 20px !important;
  color: #606266; /* 默认字体颜色 */
  transition: background-color 0.3s, color 0.3s;
}

.el-menu-item i {
  margin-right: 10px;
  color: #409eff; /* 图标颜色 */
}

.el-menu-item:hover {
  color: #409eff;
  background-color: #f2f6fc;
  cursor: pointer;
}

.el-submenu__title {
  font-size: 16px;
  padding-left: 20px !important;
  color: #606266;
}

.el-submenu:hover .el-submenu__title {
  color: #409eff;
}
</style>