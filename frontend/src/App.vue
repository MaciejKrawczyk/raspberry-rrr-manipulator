<template>
  <div class="border border-white p-10">
    <p>α</p>
    <button @mousedown="handleStart('minus')" @mouseup="handleEnd('minus')" @touchstart="handleStart('minus')" @touchend="handleEnd('minus')">-</button>
    <button @mousedown="handleStart('plus')" @mouseup="handleEnd('plus')" @touchstart="handleStart('plus')" @touchend="handleEnd('plus')">+</button>
    <div>Current Angle: {{ currentAngle }}</div>
  </div>
</template>

<script>
import io from 'socket.io-client';

export default {
  name: 'MyComponent',
  data() {
    return {
      currentAngle: 0,
    };
  },
  mounted() {
    this.socket = io('http://192.168.1.28:5000');

    this.socket.on('connect', () => {
      // console.log('Connected to the server.');
    });

    this.socket.on('response', (data) => {
      // console.log('Response from server:', data);
    });

    this.socket.on('angle_update', (data) => {
      // console.log('Angle update received:', data);
      this.currentAngle = data.angle;
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
