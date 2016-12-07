package test

import java.io.PrintWriter
import java.net.ServerSocket
import scala.io.Source

/**
 * Created by JChubby on 2015/6/29.
 * ��ȡHDFS���ݣ�����Socket���͵�Spark����
 */
object TestDataGenerator {
  def main(args: Array[String]) {
    println("=====================")
    val listener = new ServerSocket(9999)
    lazy val lines = Source.fromFile("/home/cloud/data/streamData").getLines()
    while (true) {
      val socket = listener.accept()
      new Thread() {
        override def run = {
          println("Get client connected from:" + socket.getInetAddress)
          val out = new PrintWriter(socket.getOutputStream(), true)
          while (true) {
            while (lines.hasNext) {
              val line = lines.next()
              out.write(line + '\n')
              out.flush()
              Thread.sleep(1)
            }
          }
          socket.close()
        }
      }.start()
    }
  }
}
