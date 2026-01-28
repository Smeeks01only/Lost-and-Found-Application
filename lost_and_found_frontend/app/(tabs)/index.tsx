import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, StyleSheet, ActivityIndicator, TouchableOpacity } from 'react-native';
import api from '../../services/api';
import { Item } from '../../types';

export default function HomeScreen() {
    const [items, setItems] = useState<Item[]>([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState<'lost' | 'found'>('lost');

    const fetchItems = async () => {
        setLoading(true);
        try {
            const response = await api.get(`/items/${filter}/`);
            setItems(response.data);
        } catch (error) {
            console.log('Error fetching items:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchItems();
    }, [filter]);

    const renderItem = ({ item }: { item: Item }) => (
        <View style={styles.card}>
            <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
                <Text style={styles.itemType}>{item.item_type}</Text>
                <Text style={styles.date}>{new Date(item.created_at).toLocaleDateString()}</Text>
            </View>
            <Text style={styles.description}>{item.description}</Text>
            <Text style={styles.location}>📍 {item.location}</Text>
            {item.contact_info && <Text style={styles.contact}>📞 {item.contact_info}</Text>}
        </View>
    );

    return (
        <View style={styles.container}>
            <View style={styles.filterContainer}>
                <TouchableOpacity
                    style={[styles.filterButton, filter === 'lost' && styles.activeFilter]}
                    onPress={() => setFilter('lost')}
                >
                    <Text style={[styles.filterText, filter === 'lost' && styles.activeFilterText]}>Lost Items</Text>
                </TouchableOpacity>
                <TouchableOpacity
                    style={[styles.filterButton, filter === 'found' && styles.activeFilter]}
                    onPress={() => setFilter('found')}
                >
                    <Text style={[styles.filterText, filter === 'found' && styles.activeFilterText]}>Found Items</Text>
                </TouchableOpacity>
            </View>

            {loading ? (
                <ActivityIndicator size="large" style={{ marginTop: 20 }} />
            ) : (
                <FlatList
                    data={items}
                    keyExtractor={(item) => item.id.toString()}
                    renderItem={renderItem}
                    contentContainerStyle={{ paddingBottom: 20 }}
                    ListEmptyComponent={<Text style={styles.emptyText}>No items found.</Text>}
                />
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#f0f2f5' },
    filterContainer: { flexDirection: 'row', padding: 10, backgroundColor: '#fff', marginBottom: 10 },
    filterButton: { flex: 1, padding: 12, alignItems: 'center', borderBottomWidth: 2, borderBottomColor: 'transparent' },
    activeFilter: { borderBottomColor: '#007AFF' },
    filterText: { fontSize: 16, color: '#666' },
    activeFilterText: { color: '#007AFF', fontWeight: 'bold' },
    card: { backgroundColor: '#fff', margin: 10, padding: 15, borderRadius: 10, shadowColor: '#000', shadowOpacity: 0.1, shadowRadius: 5, elevation: 2 },
    itemType: { fontWeight: 'bold', color: '#555', marginBottom: 5 },
    description: { fontSize: 16, marginBottom: 8 },
    location: { color: '#666', marginBottom: 5 },
    contact: { color: '#007AFF', marginTop: 5 },
    date: { color: '#999', fontSize: 12 },
    emptyText: { textAlign: 'center', marginTop: 30, color: '#888' }
});
