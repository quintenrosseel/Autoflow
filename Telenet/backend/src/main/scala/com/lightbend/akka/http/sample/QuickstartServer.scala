package com.lightbend.akka.http.sample

import scala.concurrent.Await
import scala.concurrent.duration.Duration
import akka.actor.{ActorRef, ActorSystem}
import akka.http.scaladsl.Http
import akka.http.scaladsl.server.Route
import akka.stream.ActorMaterializer
import autoflow.Action.{Coloring, Green, Red}
import autoflow._

//#main-class
object QuickstartServer extends App { //with UserRoutes {

  // set up ActorSystem and other dependencies here
  //#main-class
  //#server-bootstrapping
  implicit val system: ActorSystem = ActorSystem("simulation")
//  implicit val materializer: ActorMaterializer = ActorMaterializer()
  //#server-bootstrapping

//  val userRegistryActor: ActorRef = system.actorOf(UserRegistryActor.props, "userRegistryActor")

  //#main-class
  // from the UserRoutes trait
//  lazy val routes: Route = userRoutes
  //#main-class

  //#http-server
//  Http().bindAndHandle(routes, "localhost", 8080)

//  println(s"Server online at http://localhost:8080/")

//  Await.result(system.whenTerminated, Duration.Inf)
  //#http-server
  //#main-class


  val load0 = system.actorOf(LoadSensor.props(0), "load0")
  val wait0 = system.actorOf(WaitSensor.props(0), "wait0")
  val face0 = system.actorOf(Face.props(List(load0, wait0), Green))
  val load1 = system.actorOf(LoadSensor.props(1), "load1")
  val wait1 = system.actorOf(WaitSensor.props(1), "wait1")
  val face1 = system.actorOf(Face.props(List(load1, wait1), Red))
  val load2 = system.actorOf(LoadSensor.props(2), "load2")
  val wait2 = system.actorOf(WaitSensor.props(2), "wait2")
  val face2 = system.actorOf(Face.props(List(load2, wait2), Green))
  val load3 = system.actorOf(LoadSensor.props(3), "load3")
  val wait3 = system.actorOf(WaitSensor.props(3), "wait3")
  val face3 = system.actorOf(Face.props(List(load3, wait3), Red))
  val faces: List[ActorRef] = List(face0, face1, face2, face3)
  val node = system.actorOf(Node.props(faces,
    12345, 4.345, 50.432, Coloring(List(0,2), List(1,3))), "node")


}
//#main-class
