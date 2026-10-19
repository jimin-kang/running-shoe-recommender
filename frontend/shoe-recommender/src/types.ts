export type Shoe = {
    id: number
    brand: string
    model: string

    weight_g?: number
    heel_stack_mm?: number
    forefoot_stack_mm?: number
    drop_mm?: number

    use_case?: string
    terrain?: string
}


export type ShoeRecommendation = {
  shoe: Shoe;
  score: number;
  reasons: string[];
};

export type RecommendationCardProps = {
  recommendation: ShoeRecommendation;
};