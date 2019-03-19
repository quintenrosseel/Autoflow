// Calculate det of square matrix consisting of vectors vecA and vecB: [vecA, vecB]
function calcSqDet(vecA, vecB) {
  // cfr. ad - bc formula
  return (vecA.x * vecB.y - vecB.x * vecA.y)
}

// Subtract to vectors vecA and vecB
function subtrVec(vecA, vecB) {
  return {x: (vecA.x - vecB.x),
          y: (vecA.y - vecB.y)}
}

// Calculate Orientation Determinant based on 3 given vectors.
// Cfr. Slides for notation
function orientDet(vecP, vecQ, vecR){
   return calcSqDet(subtrVec(vecQ, vecP),
                    subtrVec(vecR, vecP));
}
