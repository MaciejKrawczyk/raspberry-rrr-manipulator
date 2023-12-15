<template>
  <div>
    <button @mousedown="handleStart('minus')" @mouseup="handleEnd('minus')" @touchstart="handleStart('minus')" @touchend="handleEnd('minus')">-</button>
    <button @mousedown="handleStart('plus')" @mouseup="handleEnd('plus')" @touchstart="handleStart('plus')" @touchend="handleEnd('plus')">+</button>
  </div>
</template>

<script>
import io from 'socket.io-client';

export default {
  name: 'MyComponent',
  mounted() {
    this.socket = io('192.168.1.28:5000');

    this.socket.on('response', (data) => {
      console.log(data);
    });
  },
  methods: {
    sendMessage(message, button) {
      this.socket.emit('message', { pressed: message, button: button });
    },
    handleStart(button) {
      this.sendMessage(true, button);
    },
    handleEnd(button) {
      this.sendMessage(false, button);
    }
  }
}
</script>
