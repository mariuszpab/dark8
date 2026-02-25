<script lang="ts">
  import { onMount } from 'svelte'
  let iframeEl: HTMLIFrameElement | null = null
  export let url: string | null = null
  onMount(() => {
    // placeholder - will be replaced by Tauri WebView in production
  })
</script>

<div style="flex:1; background:#fff;">
  {#if url}
    <iframe bind:this={iframeEl} src={url} style="border:0; width:100%; height:100%;"></iframe>
  {:else}
    <div style="padding:16px;">No page loaded</div>
  {/if}
</div>
