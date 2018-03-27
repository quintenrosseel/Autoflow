package com.lightbend.akka.http.sample

import akka.actor.{ Actor, ActorLogging, Props }

//#user-case-classes
final case class Update(id: String)
final case class Updates(updates: Seq[Update])
//#user-case-classes

object MapActor {
  final case object GetUpdate
  def props: Props = Props[MapActor]
}

class MapActor extends Actor with ActorLogging {
  import MapActor._

  def receive: Receive = {
    case GetUpdate => {
      log.info("Incoming Request for update")

    }
    case _ =>
      log.info("Don't know what to do :(")
  }
}

