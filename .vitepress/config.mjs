import { defineConfig } from 'vitepress'
import { repo_base, repo_url, repo_name, icon_url } from './params';

// https://vitepress.dev/reference/site-config
export default defineConfig({
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    logo: icon_url,
    editLink: {
      pattern: repo_url + 'blob/main/:path',
      text: '在 GitHub 上编辑此页面'
    },
    socialLinks: [{ icon: 'github', link: repo_url }],
    search: {
      provider: 'local',
      options: {
        detailedView: true,
      }
    },
    outline: { label: '页面导航' },
    docFooter: {
      prev: '上一页',
      next: '下一页'
    },
    returnToTopLabel: '回到顶端',
  },

  srcDir: './docs',
  base: repo_base + '/',
  title: repo_name,
  head: [['link', { rel: 'icon', href: repo_base + icon_url }]],
  cleanUrls: true,
  ignoreDeadLinks: true,
})
