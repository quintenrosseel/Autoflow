package autoflow

import akka.actor.{Actor, ActorLogging, ActorRef, Props}
import autoflow.Action.{Coloring, Green, Red}

import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration._
import scala.util.Random
import scala.collection.mutable.Map

trait Action
object Action {
  case object Green extends Action
  case object Red extends Action
  case class Coloring(green: List[Int], red: List[Int])
}

trait StateAttribute
object StateAttribute {
  case object Load extends StateAttribute
  case object Wait extends StateAttribute
}

case class StateComponent(attribute: StateAttribute, face: Int, value: Int)
case class State(comps: Set[StateComponent])

trait NodeAgent {
  this: NodeArtifact with NodeActor =>

  val a = 0.1 // low variance
  val g = 0.9 // far-sighted
  val t = 0.1 // greedy

  type Quality = Double
  var state: State = State(Set.empty[StateComponent])
  var next: State = State(Set.empty[StateComponent])
  var coloring: Coloring

  var q: Map[State, Map[Coloring, Quality]] = Map.empty

  def update(coloring: Coloring): Unit = {
    val colorings: Map[Coloring, Quality] =
      q.getOrElse(state, Map.empty[Coloring, Quality])
    val quality: Quality =
      colorings.getOrElse(coloring, 0.0)
    val prime: Quality =
      (1 - a) * quality + a * (reward(next) + g * optimal(next))

    colorings(coloring) = prime
    q = q + (state -> colorings)

    state = next
  }

  def exp(value: Double): Double =
    math.pow(math.E, value / t)

  def pr(colorings: Map[Coloring, Quality], coloring: Coloring): Double =
    exp(colorings(coloring)) /
      colorings.values.map(exp).sum

  def choose(): Coloring = {
    val r = Random nextDouble
    var sum = 0.0

    val colorings = q.getOrElse(state, Map.empty + (coloring -> 0.0) +
      (coloring match {
        case Coloring(green, red) => Coloring(red, green) -> 0.0 }))
    for ((coloring, quality) <- colorings) yield {
      sum += pr(colorings, coloring)
      if (r <= sum) {
        update(coloring)
        return coloring
      }
    }
    colorings.head._1 // this should never happen
  }

  def reward(state: State): Double =
    if (state.comps.exists(c => c.value != 0.0)) 0.0 else 100.0

  def optimal(state: State): Double = {
    val colorings: Map[Coloring, Quality] =
      q.getOrElse(state, Map.empty[Coloring, Quality])
    (0.0 /: colorings) (_ max _._2)
  }

  def updateNext(comp: StateComponent): Unit =
    next = next.copy(comps = next.comps + comp)
}

trait NodeAgentNaive {
  this: NodeArtifact with NodeActor =>

  var coloring: Coloring

  def choose(): Coloring = { coloring match {
    case Coloring(green, red) => coloring = Coloring(red, green)
  }
    coloring
  }
}

// Node
trait NodeArtifact {

  val id: Int
  val latitude: Double
  val longitude: Double
}

trait NodeActor extends Actor with ActorLogging {
  this: NodeArtifact with NodeAgent =>
  val faces: List[ActorRef]

  context.system.scheduler.schedule(
    initialDelay = 5 seconds, interval = 5 seconds, self, Tick)

  def receive = {
    case Tick =>
      val choice = choose()
      choice.green.foreach(faces(_) ! Green)
      choice.red.foreach(faces(_) ! Red)
    case comp: StateComponent => updateNext(comp)
  }
}

case class Node(faces: List[ActorRef],
                id: Int,
                latitude: Double,
                longitude: Double,
                var coloring: Coloring
               ) extends NodeArtifact with NodeActor with NodeAgent

object Node {
  def props(faces: List[ActorRef],
            id: Int,
            latitude: Double,
            longitude: Double,
            coloring: Coloring): Props =
    Props(classOf[Node], faces, id, latitude, longitude, coloring)
}

// Face
trait FaceArtifact {
//  val in: Option[InGate]
//  val out: Option[OutGate]
  var light: Action
  var process = List.empty[Int]  // each Int is a car with wait time
}

trait FaceActor extends Actor with ActorLogging {
  this: FaceArtifact =>
  val sensors: List[ActorRef]

  context.system.scheduler.schedule(
    initialDelay = 1 seconds, interval = 1 seconds, self, Tick)

  context.system.scheduler.schedule(
    initialDelay = 3 seconds, interval = 3 seconds, self, Queue)

  def receive = {
    case Tick =>
      process = if (light == Green) process.drop(1) else process
      process = process.map(_ + 1)
      sensors.foreach(_ ! Line(process))
    case Queue =>
      process = (1 :: process.reverse).reverse
    case Green => light = Green
    case Red => light = Red
    case comp: StateComponent =>
      log.info(comp.toString())
      context.actorSelection("/user/node") ! comp
  }
}

case class Face(sensors: List[ActorRef],
//                in: InGate,
//                out: OutGate,
                var light: Action
               ) extends FaceArtifact with FaceActor

object Face {
  def props(sensors: List[ActorRef], light: Action): Props =
    Props(classOf[Face], sensors, /*Some(InGate()), Some(OutGate()),*/ light)
}


// Sensor
trait SensorArtifact {
  val faceIndex: Int
  def emit(line: List[Int]): Int
  val attr: StateAttribute
}

trait SensorActor extends Actor with ActorLogging {
  this: SensorArtifact =>

  def receive = {
    case Line(line: List[Int]) =>
      sender ! StateComponent(attr, faceIndex, emit(line))
  }
}

case class LoadSensor(faceIndex: Int)
  extends SensorArtifact with SensorActor {

  def emit(line: List[Int]): Int = line.length
  val attr: StateAttribute = StateAttribute.Load
}

object LoadSensor {
  def props(faceIndex: Int): Props = Props(classOf[LoadSensor], faceIndex)
}

case class WaitSensor(faceIndex: Int)
  extends SensorArtifact with SensorActor {

  def emit(line: List[Int]): Int = line.sum
  val attr: StateAttribute = StateAttribute.Wait
}

object WaitSensor {
  def props(faceIndex: Int): Props = Props(classOf[WaitSensor], faceIndex)
}

case class InGate()
case class OutGate()

// Specific emit messages for each type of sensor ???
case class Emit(face: Int, signal: Double)
case class Line(line: List[Int])
object Tick
object Queue