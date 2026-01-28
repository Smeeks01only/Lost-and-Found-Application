export interface Item {
    id: number;
    reporter: number;
    item_type: 'LOST' | 'FOUND';
    description: string;
    location: string;
    date_lost_found: string;
    status: 'ACTIVE' | 'CLAIMED' | 'ARCHIVED';
    contact_info?: string;
    created_at: string;
    security_question?: string;
}

export interface Match {
    id: number;
    lost_item: Item;
    found_item: Item;
    score: number;
    status: 'PENDING' | 'ACCEPTED' | 'REJECTED';
    created_at: string;
}

export interface User {
    username: string;
    email?: string;
    role?: 'LOSER' | 'OFFICE' | 'TECH';
}
