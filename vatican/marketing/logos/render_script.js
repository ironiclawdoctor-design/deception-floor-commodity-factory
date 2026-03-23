const canvas = document.createElement('canvas');
canvas.width = 512;
canvas.height = 512;
const ctx = canvas.getContext('2d');

// Draw Background (The Void)
ctx.fillStyle = '#000000';
ctx.fillRect(0, 0, 512, 512);

// Draw the Golden Circle (The See)
ctx.strokeStyle = '#FFD700';
ctx.lineWidth = 15;
ctx.beginPath();
ctx.arc(256, 256, 230, 0, Math.PI * 2);
ctx.stroke();

// Draw the Master Command (Zhì)
ctx.fillStyle = '#FFD700';
ctx.font = 'bold 150px Arial';
ctx.textAlign = 'center';
ctx.fillText('制', 256, 300);

// Status Metadata
ctx.font = 'bold 30px Arial';
ctx.fillText('SOVEREIGN SEE :: 125M MASS', 256, 460);

document.body.appendChild(canvas);
