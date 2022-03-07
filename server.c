/* -*- mode: c; c-basic-offset: 2; indent-tabs-mode: nil; -*-
 *
 * Using the C-API of this library.
 *
 */
#include "led-matrix-c.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>	//inet_addr
#include <time.h> // clock

int main(int argc, char **argv) {
  struct RGBLedMatrixOptions options;
  struct RGBLedMatrix *matrix;
  struct LedCanvas *offscreen_canvas;

  int socket_desc , new_socket , c;
  struct sockaddr_in server , client;

  int width, height;
  int x, y;

  clock_t current_ticks, delta_ticks;
  clock_t fps = 0;

  memset(&options, 0, sizeof(options));
  options.rows = 16;
  options.chain_length = 1;

  /* This supports all the led commandline options. Try --led-help */
  matrix = led_matrix_create_from_options(&options, &argc, &argv);
  if (matrix == NULL) {
    puts("Failed to create matrix");
    return 1;
  }

  /* Create socket */
  socket_desc = socket(AF_INET, SOCK_STREAM, 0);
  if (socket_desc == -1) {
    puts("Could not create socket");
  }

  /* Prepare the sockaddr_in structure */
  server.sin_family = AF_INET;
  server.sin_addr.s_addr = INADDR_ANY;
  server.sin_port = htons(8888);

  /* Bind to 0.0.0.0:8888 */
  if (bind(socket_desc, (struct sockaddr *)&server, sizeof(server)) < 0) {
    puts("Failed to bind to port 8888, is it in use?");
    return 1;
  }

  listen(socket_desc, 3);

  puts("Now accepting connections on 0.0.0.0:8888");

  /* Let's do an example with double-buffering. We create one extra
   * buffer onto which we draw, which is then swapped on each refresh.
   * This is typically a good aproach for animations and such.
   */
  offscreen_canvas = led_matrix_create_offscreen_canvas(matrix);
  led_canvas_get_size(offscreen_canvas, &width, &height);

  printf("Grid %dx%d", height, width);

  c = sizeof(struct sockaddr_in);
  while ((new_socket = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c))){
    uint8_t matrix_data[height][width * 3]; // Init received matrix data array [y][x]
    char recv_buf[width * 3];
    char send_buf[1];

    puts("Connection accepted");

    while (1) {
      current_ticks = clock();

      for (y = 0; y < height; ++y) {
        // Send ENQ for sending
        send_buf[0] = 0x05;
        write(new_socket, send_buf, 1);

        // Receive line data
        recv(new_socket, recv_buf, width * 3, 0);
        for (x = 0; x < (width * 3); ++x) {
          matrix_data[y][x] = (uint8_t)(recv_buf[x]);
        }

        // Send ACK for datareceived
        send_buf[0] = 0x06;
        write(new_socket, send_buf, 1);
      }

      // Send EOT to signal end of transmission
      //send_buf[0] = 0x04;
      //write(new_socket, send_buf, 1);

      // Write matrix data to the offscreen canvas
      for (y = 0; y < height; y++) {
        for (x = 0; x < width; x++) {
          led_canvas_set_pixel(offscreen_canvas, x, y, matrix_data[y][x * 3] & 0xff, matrix_data[y][(x * 3) + 1] & 0xff, matrix_data[y][(x * 3) + 2] & 0xff);
        }
      }

      /* Now, we swap the canvas. We give swap_on_vsync the buffer we
       * just have drawn into, and wait until the next vsync happens.
       * we get back the unused buffer to which we'll draw in the next
       * iteration.
       */
      offscreen_canvas = led_matrix_swap_on_vsync(matrix, offscreen_canvas);

//      delta_ticks = clock() - current_ticks; //the time, in ms, that took to render the scene
//      if (delta_ticks > 0)
//        fps = CLOCKS_PER_SEC / delta_ticks;
//      printf("FPS: %d\n", fps);

      usleep(500);
    }
  }

  /*
   * Make sure to always call led_matrix_delete() in the end to reset the
   * display. Installing signal handlers for defined exit is a good idea.
   */
  led_matrix_delete(matrix);

  return 0;
}
