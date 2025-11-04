<template><div class="pf-card"><h3>{{ Entity }} Translations</h3>
<div class="pf-tabs"><button v-for="l in locales" :key="l" class="pf-tab" :class="{active: l===locale}" @click="switchLocale(l)">{{ l }}</button></div>
<form @submit.prevent="save"><div v-for="f in translatableFields" :key="f.name"><label>{{ f.label || f.name }}<input v-model="form[f.name]" class="pf-input"/></label></div><div class="pf-actions"><button class="pf-btn pf-primary" type="submit">Save</button></div></form></div></template>
<script setup>
import { reactive, ref } from "vue"; import { createGraphQLClient } from "../composables/useGraphQL";
const props=defineProps({ endpoint:{type:String,default:""}, id:{type:String,required:true}, locales:{type:Array,default:()=>["en","es","fr"]}, translatableFields:{type:Array,default:()=>[{ name:"name", label:"Name" }]} });
const client=createGraphQLClient(props.endpoint); const locale=ref(props.locales[0]); const form=reactive({});
const GET=`query($id:ID!,$locale:String!){ {{ entity_field }}(id:$id){ id translations(locale:$locale){ id entityId locale {% for f in translatable_fields %}{{ f.name }} {% endfor %} } } }`;
const UPSERT=`mutation($entityId:ID!,$locale:String!,$input:{{ EntityTranslationInput }}!){ {{ upsert_translation_field }}(entityId:$entityId,locale:$locale,input:$input){ id } }`;
async function load(){ const d=await client.request(GET,{id:props.id,locale:locale.value}); const tr=d["{{ entity_field }}"]?.translations||{}; {% for f in translatable_fields %}form["{{ f.name }}"]=tr["{{ f.name }}"]||""; {% endfor %} }
async function save(){ await client.request(UPSERT,{ entityId: props.id, locale: locale.value, input: form }); }
function switchLocale(l){ locale.value=l; load(); } load();
</script>
<style scoped>.pf-card{border:1px solid #ddd;border-radius:12px;padding:12px}.pf-tabs{display:flex;gap:6px;margin-bottom:8px}.pf-tab{padding:6px 10px;border:1px solid #ccc;border-radius:8px;background:#f8f8f8;cursor:pointer}.pf-tab.active{border-color:#1f6feb}label{display:block;margin:8px 0}.pf-input{width:100%;padding:8px;border:1px solid #ccc;border-radius:8px}.pf-actions{display:flex;justify-content:flex-end}.pf-btn{padding:6px 10px;border:1px solid #ccc;border-radius:8px;background:#f8f8f8;cursor:pointer}.pf-primary{border-color:#1f6feb}</style>
