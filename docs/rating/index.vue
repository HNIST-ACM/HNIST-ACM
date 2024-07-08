<template>
    <table>
        <thead>
            <tr>
                <th>年级</th>
                <td>姓名</td>
                <td><a href="https://codeforces.com">Codeforces</a></td>
                <td><a href="https://ac.nowcoder.com">Nowcoder</a></td>
                <td><a href="https://atcoder.jp">AtCoder</a></td>
            </tr>
        </thead>
        <tbody>
            <template v-for="(users, year) of info">
                <td :rowspan="users.length + 1">{{ year }}</td>
                <tr v-for="user of users">
                    <th style="white-space: nowrap;">{{ user.name }}</th>
                    <td style="white-space: nowrap;"><a v-if="user.cf.id" :href="'https://codeforces.com/profile/' + user.cf.id"
                           :style="{ color: user.cf.color }">{{
                            user.cf.id }} ({{ user.cf.rating }})</a></td>
                    <td style="white-space: nowrap;"><a v-if="user.nc.uid" :href="'https://ac.nowcoder.com/acm/contest/profile/' + user.nc.uid"
                           :style="{ color: user.nc.color }">
                            {{ user.nc.id }} ({{ user.nc.rating }})
                        </a>
                        <div v-else-if="user.nc.id"><a>{{ user.nc.id }}</a></div>
                    </td>
                    <td style="white-space: nowrap;"><a :href="'https://atcoder.jp/users/' + user.atc.id">{{ user.atc.id }}</a></td>
                </tr>
            </template>
        </tbody>
    </table>
</template>

<script setup>
import { ref } from 'vue';
import { onMounted } from 'vue';
const info = ref({});
onMounted(async () => {
    await fetch('info.json').then(res => {
        res.json().then(res => {
            info.value = res;
        });
    })
})
</script>

<style scoped>
a {
    text-decoration: none;
}
</style>