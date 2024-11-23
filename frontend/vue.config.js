module.exports = {
  devServer: {
    port:8081,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000/',
        changeOrigin: true, // 修改目标的origin为代理服务器origin
        pathRewrite: { '^/': '' }, // 重写路径，去除'/api'前缀
      },
    },
  },
};
