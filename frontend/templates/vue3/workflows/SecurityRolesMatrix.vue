<template><div class="pf-card"><h3>User Roles</h3>
<div class="pf-toolbar"><input v-model="userId" placeholder="User ID" class="pf-input"/><select v-model="role" class="pf-input"><option v-for="r in roles" :key="r" :value="r">{{ r }}</option></select><button class="pf-btn pf-primary" @click="grant">Grant</button><button class="pf-btn pf-danger" @click="revoke">Revoke</button></div>
<pre>Selected: {{ userId }} – {{ role }}</pre></div></template>
<script setup>
import { ref } from "vue"; import { createGraphQLClient } from "../composables/useGraphQL";
const props=defineProps({ endpoint:{type:String,default:""}, roles:{type:Array,default:()=>[{% for r in roles %}"{{ r }}",{% endfor %}] } });
const client=createGraphQLClient(props.endpoint); const userId=ref(""); const role=ref(props.roles[0]||"");
const GRANT=`mutation($userId:ID!,$role:{{ RoleEnum }}!){ {{ grant_role_field }}(userId:$userId,role:$role) }`; const REVOKE=`mutation($userId:ID!,$role:{{ RoleEnum }}!){ {{ revoke_role_field }}(userId:$userId,role:$role) }`;
async function grant(){ await client.request(GRANT,{userId:userId.value,role:role.value}); } async function revoke(){ await client.request(REVOKE,{userId:userId.value,role:role.value}); }
</script>
<style scoped>.pf-card{border:1px solid #ddd;border-radius:12px;padding:12px}.pf-toolbar{display:flex;gap:8px;margin-bottom:8px}.pf-input{padding:8px;border:1px solid #ccc;border-radius:8px}.pf-btn{padding:6px 10px;border:1px solid #ccc;border-radius:8px;background:#f8f8f8;cursor:pointer}.pf-primary{border-color:#1f6feb}.pf-danger{border-color:#d73a49}</style>
