package autoflow

import akka.actor.{Actor, ActorLogging, ActorRef}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration._
import scala.util.Random
import scala.collection.mutable.Map

trait Action
object Action {
  case object Green extends Action
  case object Red extends Action
  case class Green(i: Int) extends Action
  case class Red(i: Int) extends Action
}

trait StateAttribute
object StateAttribute {
  case object Load extends StateAttribute
  case object Wait extends StateAttribute
}

case class StateComponent(attribute: StateAttribute, face: Int, value: Int)
case class State(attrs: Set[StateComponent])

trait NodeAgent {
  val a = 0.1 // low variance
  val g = 0.9 // far-sighted
  val t = 0.1 // greedy

  type Quality = Double
  var state: State

  var q: Map[State, Map[Action, Quality]] = Map.empty

  def update(next: State, action: Action): Unit = {
    val actions: Map[Action, Quality] =
      q.getOrElse(state, Map.empty[Action, Quality])
    val quality: Quality =
      actions.getOrElse(action, 0.0)
    val prime: Quality =
      (1 - a) * quality + a * (reward(next) + g * optimal(next))

    actions(action) = prime
    q = q + (state -> actions)

    state = next
  }

  def exp(value: Double): Double =
    math.pow(math.E, value / t)

  def pr(actions: Map[Action, Quality], action: Action): Double =
    exp(actions(action)) / actions.keys.map(actions(_)).sum

  def choose(state: State): Action = {
    val r = Random nextDouble
    var sum = 0.0
    val actions = q(state)
    for ((action, quality) <- actions) yield {
      sum += pr(actions, action)
      if (r <= sum) return action
    }
    actions.head._1 // this should never happen
  }

//  def act(state: State): Action = {
//    val actions: Map[Action, Quality] =
//      q.getOrElse(state, Map.empty[Action, Quality])
//
//  }

  def reward(state: State): Double =
    if (state.attrs.exists(c => c.value != 0.0)) 0.0 else 100.0

  def optimal(state: State): Double = {
    val actions: Map[Action, Quality] =
      q.getOrElse(state, Map.empty[Action, Quality])
    (0.0 /: actions) (_ max _._2)
  }

  // should be in aggregator?
  //  def updateState(attr: StateAttr, value: Double): Unit = {
  //    state = state + (attr -> value)
  //  }
}

// Node
trait Node {
  val id: Int
  val latitude: Double
  val longitude: Double
  val faces: List[Face]
}

trait NodeActor extends Node with Actor with ActorLogging {

  context.system.scheduler.schedule(
    initialDelay = 5 seconds, interval = 5 seconds, self, Tick)

  def receive = {
    case Tick => ??? // act
    case emit: Emit => ??? // updateState
    case _ => log.info("node")
  }
}

// Face
trait Face {
  def emit: Double
  val in: Option[InGate]
  val out: Option[OutGate]
}

trait FaceActor extends Face with Actor with ActorLogging {
  val node: ActorRef

  def receive = {
    case emit: Emit => node ! emit
    case _ => log.info("face")
  }
}

// Sensor
trait Sensor {
  def emit: Double
}

trait SensorActor extends Sensor with Actor with ActorLogging {
  val face: ActorRef

  context.system.scheduler.schedule(
    initialDelay = 1 seconds, interval = 1 seconds, self, Tick)

  def receive = {
    case Tick => face ! Emit(emit)
    case _ => log.info("sensor")
  }
}

case class InGate()
case class OutGate()

// Specific emit messages for each type of sensor ???
case class Emit(signal: Double)
object Tick